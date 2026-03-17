<script lang="ts">
	import { api, type Coffee, type Descriptor, type Equipment, type BrewMethod, type Taster, type BasketSize } from '$lib/api';
	import { t } from '$lib/i18n';
	import StarRating from './StarRating.svelte';
	import DescriptorAutocomplete from './DescriptorAutocomplete.svelte';
	import Icons from './Icons.svelte';

	let { coffeeId, onDeleted, onUpdated }: {
		coffeeId: number;
		onDeleted: () => void;
		onUpdated: () => void;
	} = $props();

	let coffee = $state<Coffee | null>(null);
	let descriptors = $state<Descriptor[]>([]);
	let equipmentList = $state<Equipment[]>([]);
	let brewMethods = $state<BrewMethod[]>([]);
	let tasters = $state<Taster[]>([]);
	let basketSizes = $state<BasketSize[]>([]);
	let loading = $state(true);

	// Review form
	let editingReviewTasterId = $state<number | null>(null);
	let reviewRating = $state(0);
	let reviewComment = $state('');
	let reviewDescriptors = $state<number[]>([]);

	// Grinder setting form
	let showSettingForm = $state(false);
	let settingValue = $state('');
	let settingNotes = $state('');
	let settingBasketId = $state<number | null>(null);

	async function loadData() {
		loading = true;
		const [c, d, eq, bm, ta, bs] = await Promise.all([
			api.coffees.get(coffeeId),
			api.descriptors.list(),
			api.equipment.list(),
			api.equipment.brewMethods(),
			api.tasters.list(),
			api.equipment.basketSizes(),
		]);
		coffee = c;
		descriptors = d;
		equipmentList = eq;
		brewMethods = bm;
		tasters = ta;
		basketSizes = bs;
		loading = false;
	}

	$effect(() => { coffeeId; loadData(); });

	const suggestedDescriptorIds = $derived(
		coffee?.roastery_descriptors.map(d => d.id) ?? []
	);

	// Tasters who haven't reviewed yet
	const unreviewedTasters = $derived(
		tasters.filter(ta => !coffee?.reviews.some(r => r.taster_id === ta.id))
	);

	function startReview(tasterId: number, existing?: { rating: number; comment: string | null; descriptors: { id: number }[] }) {
		editingReviewTasterId = tasterId;
		reviewRating = existing?.rating ?? 0;
		reviewComment = existing?.comment ?? '';
		reviewDescriptors = existing?.descriptors.map(d => d.id) ?? [];
	}

	function cancelReview() {
		editingReviewTasterId = null;
		reviewRating = 0;
		reviewComment = '';
		reviewDescriptors = [];
	}

	function toggleReviewDescriptor(id: number) {
		if (reviewDescriptors.includes(id)) {
			reviewDescriptors = reviewDescriptors.filter(d => d !== id);
		} else {
			reviewDescriptors = [...reviewDescriptors, id];
		}
	}

	async function saveReview() {
		if (!editingReviewTasterId || reviewRating === 0) return;
		await api.reviews.upsert(coffeeId, {
			taster_id: editingReviewTasterId,
			rating: reviewRating,
			comment: reviewComment.trim() || undefined,
			descriptor_ids: reviewDescriptors.length > 0 ? reviewDescriptors : undefined,
		});
		cancelReview();
		await loadData();
		onUpdated();
	}

	async function deleteReview(reviewId: number) {
		await api.reviews.delete(coffeeId, reviewId);
		await loadData();
		onUpdated();
	}

	async function toggleAvailability() {
		if (!coffee) return;
		await api.coffees.update(coffeeId, { is_available: !coffee.is_available });
		await loadData();
		onUpdated();
	}

	async function addGrinderSetting() {
		const grinder = equipmentList.find(e => e.type === 'grinder' && e.is_default) || equipmentList.find(e => e.type === 'grinder');
		const method = brewMethods.find(m => m.is_default) || brewMethods[0];
		if (!grinder || !method || !settingValue) return;
		await api.grinderSettings.create(coffeeId, {
			equipment_id: grinder.id,
			brew_method_id: method.id,
			basket_size_id: settingBasketId ?? undefined,
			setting: parseFloat(settingValue),
			notes: settingNotes.trim() || undefined,
		});
		settingValue = '';
		settingNotes = '';
		settingBasketId = null;
		showSettingForm = false;
		await loadData();
		onUpdated();
	}

	async function deleteGrinderSetting(settingId: number) {
		await api.grinderSettings.delete(coffeeId, settingId);
		await loadData();
		onUpdated();
	}

	async function deleteCoffee() {
		if (!confirm($t('detail.delete_confirm'))) return;
		await api.coffees.delete(coffeeId);
		onDeleted();
	}
</script>

{#if loading}
	<div class="flex items-center justify-center h-full">
		<div class="text-stone-300">Loading...</div>
	</div>
{:else if coffee}
	<div class="p-6 space-y-5">
		<!-- Header with availability toggle -->
		<div class="flex items-start justify-between">
			<div class="flex items-center gap-3">
				<h2 class="text-2xl font-bold text-stone-800" style="font-family: 'DM Serif Display', serif;">
					{coffee.name}
				</h2>
				<button onclick={toggleAvailability}
					class="px-2 py-0.5 rounded text-xs font-medium transition-colors
						{coffee.is_available
							? 'bg-green-100 text-green-700 hover:bg-green-200'
							: 'bg-stone-100 text-stone-400 hover:bg-stone-200'}"
				>
					{coffee.is_available ? 'Have it' : 'Out'}
				</button>
			</div>
			<button onclick={deleteCoffee} class="p-2 text-stone-300 hover:text-red-500 transition-colors" title={$t('detail.delete')}>
				<Icons icon="delete" size={18} />
			</button>
		</div>

		<!-- Coffee info — horizontal layout -->
		<div class="bg-white rounded-2xl border border-stone-100 shadow-sm overflow-hidden">
			<div class="flex">
				{#if coffee.image_url}
					<div class="bg-stone-50 p-5 flex items-center justify-center border-r border-stone-100 flex-shrink-0" style="width: 200px;">
						<img src={coffee.image_url} alt={coffee.name} class="max-h-40 object-contain" />
					</div>
				{/if}
				<div class="p-5 flex-1 space-y-3">
					<p class="text-sm text-stone-400">{coffee.roastery}</p>
					<div class="flex flex-wrap gap-x-6 gap-y-1 text-sm">
						{#if coffee.origin}
							<div><span class="text-stone-300 text-xs uppercase tracking-wide">{$t('detail.origin')}</span><p class="text-stone-700 font-medium">{coffee.origin}</p></div>
						{/if}
						{#if coffee.process}
							<div><span class="text-stone-300 text-xs uppercase tracking-wide">{$t('detail.process')}</span><p class="text-stone-700 font-medium">{coffee.process}</p></div>
						{/if}
						{#if coffee.roast_level}
							<div><span class="text-stone-300 text-xs uppercase tracking-wide">{$t('detail.roast')}</span><p class="text-stone-700 font-medium">{coffee.roast_level}</p></div>
						{/if}
					</div>
					{#if coffee.score || coffee.sweetness || coffee.acidity || coffee.bitterness}
						<div class="flex gap-5">
							{#if coffee.score}<div><span class="text-xl font-bold text-amber-700">{coffee.score}</span><span class="text-[10px] text-stone-300 ml-1">{$t('detail.score')}</span></div>{/if}
							{#if coffee.sweetness}<div><span class="text-sm font-semibold">{coffee.sweetness}</span><span class="text-[10px] text-stone-300 ml-1">{$t('detail.sweet')}</span></div>{/if}
							{#if coffee.acidity}<div><span class="text-sm font-semibold">{coffee.acidity}</span><span class="text-[10px] text-stone-300 ml-1">{$t('detail.acid')}</span></div>{/if}
							{#if coffee.bitterness}<div><span class="text-sm font-semibold">{coffee.bitterness}</span><span class="text-[10px] text-stone-300 ml-1">{$t('detail.bitter')}</span></div>{/if}
						</div>
					{/if}
					{#if coffee.roastery_descriptors.length > 0}
						<div class="flex flex-wrap gap-1.5">
							{#each coffee.roastery_descriptors as desc}
								<span class="px-2 py-0.5 rounded-full text-xs bg-amber-50 text-amber-700 border border-amber-100">{desc.name}</span>
							{/each}
						</div>
					{/if}
					{#if coffee.roastery_url}
						<a href={coffee.roastery_url} target="_blank" rel="noopener" class="inline-flex items-center gap-1.5 text-xs text-amber-600 hover:text-amber-800">
							<Icons icon="link" size={12} /> {$t('detail.roastery_link')}
						</a>
					{/if}
				</div>
			</div>
		</div>

		<!-- Two-column: Grinder + Reviews -->
		<div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
			<!-- Grinder Settings -->
			<div class="bg-white rounded-2xl border border-stone-100 shadow-sm p-5">
				<div class="flex items-center justify-between mb-3">
					<div class="flex items-center gap-2">
						<Icons icon="grinder" size={16} className="text-stone-400" />
						<h3 class="font-semibold text-sm text-stone-700">{$t('grinder.title')}</h3>
					</div>
					{#if !showSettingForm}
						<button onclick={() => showSettingForm = true} class="text-xs text-amber-600 hover:text-amber-800 font-medium">{$t('grinder.add')}</button>
					{/if}
				</div>
				{#if coffee.grinder_settings.length === 0 && !showSettingForm}
					<p class="text-sm text-stone-300">{$t('grinder.no_setting')}</p>
				{/if}
				{#each coffee.grinder_settings as setting}
					<div class="flex items-center justify-between py-2 border-b border-stone-50 last:border-0">
						<div class="flex items-center gap-3">
							<span class="text-2xl font-bold text-amber-700 tabular-nums">{setting.setting}</span>
							<div class="text-xs text-stone-400">
								<p>{setting.brew_method.name}{#if setting.basket_size} &middot; {setting.basket_size.label}{/if}</p>
							</div>
						</div>
						<button onclick={() => deleteGrinderSetting(setting.id)} class="p-1 text-stone-200 hover:text-red-400 transition-colors" title={$t('detail.delete')}>
							<Icons icon="delete" size={14} />
						</button>
					</div>
				{/each}
				{#if showSettingForm}
					<div class="mt-2 p-3 bg-stone-50 rounded-xl space-y-2">
						<div class="flex gap-2">
							<input type="number" step="0.5" bind:value={settingValue} placeholder="12.5"
								class="w-20 px-2 py-1.5 rounded border border-stone-200 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-amber-400/50" />
							<select bind:value={settingBasketId} class="px-2 py-1.5 rounded border border-stone-200 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-amber-400/50">
								<option value={null}>{$t('grinder.basket')}</option>
								{#each basketSizes as bs}<option value={bs.id}>{bs.label}</option>{/each}
							</select>
							<input type="text" bind:value={settingNotes} placeholder={$t('grinder.notes')}
								class="flex-1 px-2 py-1.5 rounded border border-stone-200 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-amber-400/50" />
						</div>
						<div class="flex gap-2">
							<button onclick={addGrinderSetting} class="px-3 py-1.5 bg-amber-700 text-white rounded text-xs hover:bg-amber-800">{$t('grinder.save')}</button>
							<button onclick={() => showSettingForm = false} class="px-3 py-1.5 text-stone-400 text-xs">{$t('grinder.cancel')}</button>
						</div>
					</div>
				{/if}
			</div>

			<!-- Reviews -->
			<div class="bg-white rounded-2xl border border-stone-100 shadow-sm p-5">
				<div class="flex items-center justify-between mb-3">
					<div class="flex items-center gap-2">
						<Icons icon="cup" size={16} className="text-stone-400" />
						<h3 class="font-semibold text-sm text-stone-700">{$t('tasting.title')}</h3>
					</div>
					{#if unreviewedTasters.length > 0 && editingReviewTasterId === null}
						<select
							onchange={(e) => { const v = parseInt((e.target as HTMLSelectElement).value); if (v) startReview(v); }}
							class="text-xs text-amber-600 bg-transparent border-none cursor-pointer focus:outline-none"
						>
							<option value="">{$t('tasting.add')}</option>
							{#each unreviewedTasters as ta}<option value={ta.id}>{ta.name}</option>{/each}
						</select>
					{/if}
				</div>

				{#if coffee.reviews.length === 0 && editingReviewTasterId === null}
					<p class="text-sm text-stone-300">{$t('tasting.empty')}</p>
				{/if}

				{#each coffee.reviews as review}
					{#if editingReviewTasterId === review.taster_id}
						<!-- Editing existing review -->
						<div class="py-2 space-y-2">
							<p class="text-sm font-medium text-stone-700">{review.taster.name}</p>
							<div class="flex items-center gap-2">
								<StarRating rating={reviewRating} interactive onRate={(v) => reviewRating = v} />
								{#if reviewRating > 0}<span class="text-xs text-stone-400 tabular-nums">{reviewRating}/10</span>{/if}
							</div>
							<textarea bind:value={reviewComment} rows={2} placeholder={$t('tasting.comment_placeholder')}
								class="w-full px-2 py-1.5 rounded border border-stone-200 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-amber-400/50 resize-none"></textarea>
							<DescriptorAutocomplete {descriptors} selected={reviewDescriptors} suggested={suggestedDescriptorIds} onToggle={toggleReviewDescriptor} />
							<div class="flex gap-2">
								<button onclick={saveReview} disabled={reviewRating === 0}
									class="px-3 py-1.5 bg-amber-700 text-white rounded text-xs hover:bg-amber-800 disabled:opacity-50">{$t('tasting.save')}</button>
								<button onclick={cancelReview} class="px-3 py-1.5 text-stone-400 text-xs">{$t('tasting.cancel')}</button>
							</div>
						</div>
					{:else}
						<!-- Display review -->
						<div class="py-2 border-b border-stone-50 last:border-0">
							<div class="flex items-center justify-between">
								<div class="flex items-center gap-2">
									<span class="text-sm font-medium text-stone-700">{review.taster.name}</span>
									<StarRating rating={review.rating} />
									<span class="text-xs text-stone-300 tabular-nums">{review.rating}/10</span>
								</div>
								<div class="flex gap-1">
									<button onclick={() => startReview(review.taster_id, review)} class="px-1.5 py-0.5 text-[10px] text-stone-300 hover:text-amber-600 transition-colors">edit</button>
									<button onclick={() => deleteReview(review.id)} class="p-1 text-stone-200 hover:text-red-400 transition-colors" title={$t('detail.delete')}>
										<Icons icon="delete" size={12} />
									</button>
								</div>
							</div>
							{#if review.comment}<p class="text-sm text-stone-500 mt-1">{review.comment}</p>{/if}
							{#if review.descriptors.length > 0}
								<div class="flex flex-wrap gap-1 mt-1">
									{#each review.descriptors as desc}
										<span class="px-1.5 py-0.5 rounded-full text-[10px] bg-stone-50 text-stone-500 border border-stone-100">{desc.name}</span>
									{/each}
								</div>
							{/if}
						</div>
					{/if}
				{/each}

				{#if editingReviewTasterId && !coffee.reviews.some(r => r.taster_id === editingReviewTasterId)}
					<!-- New review form -->
					<div class="py-2 space-y-2">
						<p class="text-sm font-medium text-stone-700">{tasters.find(ta => ta.id === editingReviewTasterId)?.name}</p>
						<div class="flex items-center gap-2">
							<StarRating rating={reviewRating} interactive onRate={(v) => reviewRating = v} />
							{#if reviewRating > 0}<span class="text-xs text-stone-400 tabular-nums">{reviewRating}/10</span>{/if}
						</div>
						<textarea bind:value={reviewComment} rows={2} placeholder={$t('tasting.comment_placeholder')}
							class="w-full px-2 py-1.5 rounded border border-stone-200 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-amber-400/50 resize-none"></textarea>
						<DescriptorAutocomplete {descriptors} selected={reviewDescriptors} suggested={suggestedDescriptorIds} onToggle={toggleReviewDescriptor} />
						<div class="flex gap-2">
							<button onclick={saveReview} disabled={reviewRating === 0}
								class="px-3 py-1.5 bg-amber-700 text-white rounded text-xs hover:bg-amber-800 disabled:opacity-50">{$t('tasting.save')}</button>
							<button onclick={cancelReview} class="px-3 py-1.5 text-stone-400 text-xs">{$t('tasting.cancel')}</button>
						</div>
					</div>
				{/if}
			</div>
		</div>

		{#if coffee.notes}
			<p class="text-sm text-stone-400 italic">{coffee.notes}</p>
		{/if}
	</div>
{/if}
