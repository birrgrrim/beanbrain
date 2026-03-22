<script lang="ts">
	import { api, type Coffee, type Descriptor, type Grinder, type BrewSetup, type Taster, type Origin, type Roastery } from '$lib/api';
	import { refData } from '$lib/refData';
	import { toggleId } from '$lib/utils';
	import { t } from '$lib/i18n';
	import { lang } from '$lib/lang';
	import { activePerson } from '$lib/personStore';
	import { activeGrinder, activeBrewSetup } from '$lib/contextStore';
	import StarRating from './StarRating.svelte';
	import DescriptorAutocomplete from './DescriptorAutocomplete.svelte';
	import ReviewForm from './ReviewForm.svelte';
	import GrindValue from './GrindValue.svelte';
	import Icons from './Icons.svelte';

	let currentLang = $state('en');
	lang.subscribe(v => currentLang = v);

	let { coffeeId, onDeleted, onUpdated, onBack }: {
		coffeeId: number;
		onDeleted: () => void;
		onUpdated: () => void;
		onBack: () => void;
	} = $props();

	let coffee = $state<Coffee | null>(null);
	let descriptors = $state<Descriptor[]>([]);
	let grindersList = $state<Grinder[]>([]);
	let brewSetupsList = $state<BrewSetup[]>([]);
	let tasters = $state<Taster[]>([]);
	let loading = $state(true);

	let currentPersonId = $state<number | null>(null);
	let currentGrinderId = $state<number | null>(null);
	let currentBrewSetupId = $state<number | null>(null);
	activePerson.subscribe(v => currentPersonId = v);
	activeGrinder.subscribe(v => currentGrinderId = v);
	activeBrewSetup.subscribe(v => currentBrewSetupId = v);

	let originsList = $state<Origin[]>([]);
	let roasteriesList = $state<Roastery[]>([]);

	// Edit mode
	let editing = $state(false);
	let editName = $state('');
	let editRoasteryId = $state<number | null>(null);
	let editOriginId = $state<number | null>(null);
	let editProcess = $state('');
	let editRoastLevel = $state('');
	let editNotes = $state('');
	let editScore = $state<number | undefined>();
	let editSweetness = $state<number | undefined>();
	let editAcidity = $state<number | undefined>();
	let editBitterness = $state<number | undefined>();
	let editPrice = $state<number | undefined>();
	let editPriceWholesale = $state<number | undefined>();
	let editDescriptorIds = $state<number[]>([]);
	let saving = $state(false);
	let refreshing = $state(false);
	let refreshError = $state('');

	// Review form
	let editingReviewTasterId = $state<number | null>(null);
	let reviewBrewSetupId = $state<number | null>(null);
	let reviewRating = $state(0);
	let reviewComment = $state('');
	let reviewDescriptors = $state<number[]>([]);

	// Grinder setting form
	let showSettingForm = $state(false);
	let settingValue = $state('');
	let settingNotes = $state('');
	let settingGrinderId = $state<number | null>(null);
	let settingBrewSetupId = $state<number | null>(null);

	async function loadData() {
		loading = true;
		const [c, d, gr, bs, ta, ori, roast] = await Promise.all([
			api.coffees.get(coffeeId),
			refData.descriptors(),
			refData.grinders(),
			refData.brewSetups(),
			refData.tasters(),
			refData.origins(),
			refData.roasteries(),
		]);
		coffee = c;
		descriptors = d;
		grindersList = gr;
		brewSetupsList = bs;
		tasters = ta;
		originsList = ori;
		roasteriesList = roast;


		loading = false;
	}

	$effect(() => { coffeeId; editing = false; loadData(); });

	const suggestedDescriptorIds = $derived(
		coffee?.roastery_descriptors.map(d => d.id) ?? []
	);

	// Active context: find existing grind setting and review for current combo
	const activeGrindSetting = $derived(
		coffee?.grinder_settings.find(s =>
			s.grinder_id === Number(currentGrinderId) && s.brew_setup_id === Number(currentBrewSetupId)
		) ?? null
	);

	const activeReview = $derived(
		coffee?.reviews.find(r =>
			r.taster_id === Number(currentPersonId) && r.brew_setup_id === Number(currentBrewSetupId)
		) ?? null
	);

	const currentGrinderObj = $derived(grindersList.find(g => g.id === Number(currentGrinderId)));
	const currentSetupObj = $derived(brewSetupsList.find(s => s.id === Number(currentBrewSetupId)));

	const roasterCommentText = $derived(
		coffee?.roaster_comment?.[currentLang] || coffee?.roaster_comment?.['uk'] || coffee?.roaster_comment?.['en'] || null
	);


	// Edit mode helpers
	function startEditing() {
		if (!coffee) return;
		editName = coffee.name;
		editRoasteryId = coffee.roastery_id;
		editOriginId = coffee.origin_id;
		editProcess = coffee.process ?? '';
		editRoastLevel = coffee.roast_level ?? '';
		editNotes = coffee.notes ?? '';
		editScore = coffee.score ?? undefined;
		editSweetness = coffee.sweetness ?? undefined;
		editAcidity = coffee.acidity ?? undefined;
		editBitterness = coffee.bitterness ?? undefined;
		editPrice = coffee.price ?? undefined;
		editPriceWholesale = coffee.price_wholesale ?? undefined;
		editDescriptorIds = coffee.roastery_descriptors.map(d => d.id);
		editing = true;
	}

	function cancelEditing() {
		editing = false;
	}

	function toggleEditDescriptor(id: number) {
		editDescriptorIds = toggleId(editDescriptorIds, id);
	}

	async function saveEditing() {
		if (!editName.trim() || !editRoasteryId) return;
		saving = true;
		try {
			await api.coffees.update(coffeeId, {
				name: editName.trim(),
				roastery_id: editRoasteryId,
				origin_id: editOriginId || null,
				process: editProcess.trim() || null,
				roast_level: editRoastLevel.trim() || null,
				notes: editNotes.trim() || null,
				score: editScore ?? null,
				sweetness: editSweetness != null ? Math.round(editSweetness) : null,
				acidity: editAcidity != null ? Math.round(editAcidity) : null,
				bitterness: editBitterness != null ? Math.round(editBitterness) : null,
				price: editPrice != null ? Math.round(editPrice) : null,
				price_wholesale: editPriceWholesale != null ? Math.round(editPriceWholesale) : null,
				roastery_descriptor_ids: editDescriptorIds,
			});
			editing = false;
			await loadData();
			onUpdated();
		} finally {
			saving = false;
		}
	}

	// Review helpers
	function startReview(tasterId: number, brewSetupId?: number, existing?: { rating: number; comment: string | null; descriptors: { id: number }[] }) {
		editingReviewTasterId = tasterId;
		reviewBrewSetupId = brewSetupId ?? currentBrewSetupId ?? brewSetupsList[0]?.id ?? null;
		reviewRating = existing?.rating ?? 0;
		reviewComment = existing?.comment ?? '';
		reviewDescriptors = existing?.descriptors.map(d => d.id) ?? [];
	}

	function cancelReview() {
		editingReviewTasterId = null;
		reviewBrewSetupId = null;
		reviewRating = 0;
		reviewComment = '';
		reviewDescriptors = [];
	}

	async function saveReview() {
		if (!editingReviewTasterId || !reviewBrewSetupId || reviewRating === 0) return;
		await api.reviews.upsert(coffeeId, {
			taster_id: editingReviewTasterId,
			brew_setup_id: reviewBrewSetupId,
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

	async function toggleInStock() {
		if (!coffee) return;
		await api.coffees.update(coffeeId, { in_stock: !coffee.in_stock });
		await loadData();
		onUpdated();
	}

	async function toggleInStore() {
		if (!coffee) return;
		await api.coffees.update(coffeeId, { in_store: !coffee.in_store });
		await loadData();
		onUpdated();
	}

	async function addGrinderSetting() {
		if (!currentGrinderId || !currentBrewSetupId || !settingValue) return;
		// Delete existing setting for this combo first (upsert)
		if (activeGrindSetting) {
			await api.grinderSettings.delete(coffeeId, activeGrindSetting.id);
		}
		await api.grinderSettings.create(coffeeId, {
			grinder_id: Number(currentGrinderId),
			brew_setup_id: Number(currentBrewSetupId),
			setting: parseFloat(settingValue),
			notes: settingNotes.trim() || undefined,
		});
		settingValue = '';
		settingNotes = '';
		showSettingForm = false;
		await loadData();
		onUpdated();
	}

	async function deleteGrinderSetting(settingId: number) {
		await api.grinderSettings.delete(coffeeId, settingId);
		await loadData();
		onUpdated();
	}

	async function refreshCoffee() {
		if (!coffee?.roastery_url) return;
		refreshing = true;
		refreshError = '';
		try {
			await api.coffees.refresh(coffeeId);
			await loadData();
			onUpdated();
		} catch (e) {
			refreshError = e instanceof Error ? e.message : 'Refresh failed';
		} finally {
			refreshing = false;
		}
	}

	async function deleteCoffee() {
		if (!confirm($t('detail.delete_confirm'))) return;
		await api.coffees.delete(coffeeId);
		onDeleted();
	}

	const inputClass = "w-full px-3 py-1.5 rounded-lg border border-stone-200 text-sm bg-card focus:outline-none focus:ring-2 focus:ring-amber-400/50";
	const smallInputClass = "w-20 px-2 py-1.5 rounded border border-stone-200 text-sm bg-card focus:outline-none focus:ring-2 focus:ring-amber-400/50 text-center";
</script>

{#if loading}
	<div class="max-w-6xl mx-auto p-3 md:p-5 lg:p-10 space-y-3 md:space-y-4 lg:space-y-6">
		<!-- Header skeleton -->
		<div class="flex items-center gap-3">
			<div class="skeleton w-8 h-8 rounded-full"></div>
			<div class="skeleton h-7 w-48 md:w-64"></div>
		</div>
		<!-- Photo + Details skeleton -->
		<div class="grid grid-cols-1 xl:grid-cols-[1fr_2fr] gap-4 md:gap-6">
			<div class="bg-card rounded-2xl border border-stone-100 shadow-sm p-6 flex items-center justify-center">
				<div class="skeleton w-full h-48 rounded-xl"></div>
			</div>
			<div class="bg-card rounded-2xl border border-stone-100 shadow-sm p-4 md:p-6 space-y-4">
				<div class="skeleton h-5 w-36"></div>
				<div class="grid grid-cols-3 gap-3">
					<div class="skeleton h-4 w-full"></div>
					<div class="skeleton h-4 w-full"></div>
					<div class="skeleton h-4 w-full"></div>
				</div>
				<div class="flex gap-4">
					<div class="skeleton h-4 w-16"></div>
					<div class="skeleton h-4 w-16"></div>
					<div class="skeleton h-4 w-16"></div>
				</div>
				<div class="skeleton h-4 w-3/4"></div>
			</div>
		</div>
		<!-- Grinder + Reviews skeleton -->
		<div class="detail-bottom-grid">
			<div class="bg-card rounded-2xl border border-stone-100 shadow-sm p-4 md:p-6 space-y-3">
				<div class="skeleton h-5 w-32"></div>
				<div class="skeleton h-4 w-full"></div>
				<div class="skeleton h-4 w-2/3"></div>
			</div>
			<div class="bg-card rounded-2xl border border-stone-100 shadow-sm p-4 md:p-6 space-y-3">
				<div class="skeleton h-5 w-28"></div>
				<div class="skeleton h-4 w-full"></div>
				<div class="skeleton h-4 w-1/2"></div>
			</div>
		</div>
	</div>
{:else if coffee}
	<div class="detail-page">
		<!-- Header buttons -->
		<div class="flex items-center justify-between">
			<button onclick={onBack}
				class="flex items-center gap-1 px-2 py-1 md:px-3 md:py-1.5 rounded-lg text-sm font-semibold
					bg-stone-100 text-stone-600 hover:bg-stone-200 border border-stone-200">
				<Icons icon="back" size={14} />
				<span class="hidden md:inline">{$t('common.back')}</span>
			</button>
			<div class="flex items-center gap-1.5">
				{#if !editing && !coffee.roastery_url}
					<button onclick={startEditing}
						class="flex items-center gap-1 px-2 py-1 md:px-3 md:py-1.5 rounded-lg text-sm font-semibold
							bg-amber-50 text-amber-700 hover:bg-amber-100 border border-amber-200">
						<Icons icon="edit" size={14} />
						<span class="hidden md:inline">{$t('detail.edit')}</span>
					</button>
				{/if}
				<button onclick={deleteCoffee}
					class="flex items-center gap-1 px-2 py-1 md:px-3 md:py-1.5 rounded-lg text-sm font-semibold
						bg-red-50 text-red-600 hover:bg-red-100 border border-red-200"
					title={$t('detail.delete')}>
					<svg viewBox="0 0 20 20" fill="currentColor" class="w-4 h-4"><path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" /></svg>
					<span class="hidden md:inline">{$t('detail.delete')}</span>
				</button>
			</div>
		</div>

		<!-- Coffee details card -->
		<div class="bg-card rounded-xl border border-stone-100 shadow-sm animate-card overflow-hidden">
			<div class="p-3 md:p-4 lg:p-6 space-y-2 md:space-y-3 lg:space-y-4 min-w-0">
					{#if editing}
						<!-- Edit mode -->
						<input type="text" bind:value={editName}
							class="text-xl md:text-2xl font-bold text-stone-800 bg-transparent border-b-2 border-amber-300 focus:outline-none focus:border-amber-500 px-1 min-w-0 w-full"
							style="font-family: 'DM Serif Display', serif;" />
						<div class="flex flex-wrap items-center justify-between gap-3">
							<select bind:value={editRoasteryId}
								class="{inputClass} max-w-[250px]">
								{#each roasteriesList as r}
									<option value={r.id}>{r.name}</option>
								{/each}
							</select>
							<div class="flex items-center gap-4 md:gap-6">
								<div class="flex items-center gap-2">
									<button onclick={toggleInStock} aria-label="Toggle in stock"
										class="relative inline-flex h-5 w-10 items-center rounded-full transition-colors
											{coffee.in_stock ? 'bg-amber-600' : 'bg-stone-300'}">
										<span class="inline-block h-3.5 w-3.5 rounded-full bg-white shadow transition-transform
											{coffee.in_stock ? 'translate-x-5.5' : 'translate-x-0.5'}"></span>
									</button>
									<span class="text-xs text-stone-500">{$t('detail.in_stock')}</span>
								</div>
								<div class="flex items-center gap-2">
									<button onclick={coffee.roastery_url ? undefined : toggleInStore} aria-label="Toggle in store"
										class="relative inline-flex h-5 w-10 items-center rounded-full transition-colors
											{coffee.in_store ? 'bg-amber-600' : 'bg-stone-300'}
											{coffee.roastery_url ? 'opacity-50 cursor-not-allowed' : ''}">
										<span class="inline-block h-3.5 w-3.5 rounded-full bg-white shadow transition-transform
											{coffee.in_store ? 'translate-x-5.5' : 'translate-x-0.5'}"></span>
									</button>
									<span class="text-xs text-stone-500">{$t('detail.in_store')}</span>
								</div>
							</div>
						</div>
						<div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
							<div>
								<label for="edit-origin" class="text-stone-400 text-xs uppercase tracking-wide">{$t('detail.origin')}</label>
								<select id="edit-origin" bind:value={editOriginId} class={inputClass}>
									<option value={null}>—</option>
									{#each originsList as o}
										<option value={o.id}>{o.flag ? o.flag + ' ' : ''}{currentLang === 'uk' ? o.name_uk : o.name_en}</option>
									{/each}
								</select>
							</div>
							<div>
								<label for="edit-process" class="text-stone-400 text-xs uppercase tracking-wide">{$t('detail.process')}</label>
								<input id="edit-process" type="text" bind:value={editProcess} placeholder="Washed" class={inputClass} />
							</div>
							<div>
								<label for="edit-roast" class="text-stone-400 text-xs uppercase tracking-wide">{$t('detail.roast')}</label>
								<input id="edit-roast" type="text" bind:value={editRoastLevel} placeholder="Light" class={inputClass} />
							</div>
						</div>
						<div class="flex flex-wrap gap-3 md:gap-4 items-end">
							<div>
								<label for="edit-score" class="text-stone-400 text-xs uppercase tracking-wide">{$t('detail.score')}</label>
								<input id="edit-score" type="number" min="0" max="100" step="0.25" bind:value={editScore} placeholder="—" class={smallInputClass} />
							</div>
							<div>
								<label for="edit-sweet" class="text-stone-400 text-xs uppercase tracking-wide">{$t('detail.sweet')}</label>
								<input id="edit-sweet" type="number" min="1" max="10" bind:value={editSweetness} placeholder="—" class={smallInputClass} />
							</div>
							<div>
								<label for="edit-acid" class="text-stone-400 text-xs uppercase tracking-wide">{$t('detail.acid')}</label>
								<input id="edit-acid" type="number" min="1" max="10" bind:value={editAcidity} placeholder="—" class={smallInputClass} />
							</div>
							<div>
								<label for="edit-bitter" class="text-stone-400 text-xs uppercase tracking-wide">{$t('detail.bitter')}</label>
								<input id="edit-bitter" type="number" min="1" max="10" bind:value={editBitterness} placeholder="—" class={smallInputClass} />
							</div>
							<div>
								<label for="edit-price" class="text-stone-400 text-xs uppercase tracking-wide">{$t('detail.price')}</label>
								<input id="edit-price" type="number" min="0" bind:value={editPrice} placeholder="₴" class={smallInputClass} />
							</div>
							<div>
								<label for="edit-price-ws" class="text-stone-400 text-xs uppercase tracking-wide">{$t('detail.price_wholesale')}</label>
								<input id="edit-price-ws" type="number" min="0" bind:value={editPriceWholesale} placeholder="₴" class={smallInputClass} />
							</div>
						</div>
						<div>
							<span class="text-stone-400 text-xs uppercase tracking-wide">{$t('add.descriptors')}</span>
							<div class="mt-1">
								<DescriptorAutocomplete {descriptors} selected={editDescriptorIds} onToggle={toggleEditDescriptor} />
							</div>
						</div>
						<div>
							<label for="edit-notes" class="text-stone-400 text-xs uppercase tracking-wide">{$t('add.notes')}</label>
							<textarea id="edit-notes" bind:value={editNotes} rows={2} placeholder="Any notes..."
								class="w-full mt-1 px-3 py-1.5 rounded-lg border border-stone-200 text-sm bg-card focus:outline-none focus:ring-2 focus:ring-amber-400/50 resize-none"></textarea>
						</div>
						<div class="flex gap-2 pt-1">
							<button onclick={saveEditing} disabled={saving || !editName.trim() || !editRoasteryId}
								class="px-5 py-2 bg-amber-700 text-white rounded-lg text-sm hover:bg-amber-800 disabled:opacity-50">
								{saving ? $t('add.saving') : $t('common.save')}
							</button>
							<button onclick={cancelEditing} class="px-5 py-2 text-stone-400 text-sm">{$t('common.cancel')}</button>
						</div>
					{:else}
						<!-- Display mode -->
						<!-- Row 1: Name+country | store+price / quantity -->
						<div class="detail-header-grid">
							<div>
								<h2 class="text-lg md:text-xl lg:text-2xl font-bold text-stone-800 truncate" style="font-family: 'DM Serif Display', serif;">
									{#if coffee.origin_ref?.flag}<span class="mr-1">{coffee.origin_ref.flag}</span>{/if}
									{coffee.name}
								</h2>
								{#if coffee.origin_ref}
									<p class="text-xs md:text-sm text-stone-400">{currentLang === 'uk' ? coffee.origin_ref.name_uk : coffee.origin_ref.name_en}</p>
								{/if}
							</div>
							<div class="flex flex-col items-end gap-0.5">
								<div class="flex items-center gap-2">
									{#if coffee.in_store}
										<span class="inline-flex items-center gap-1 text-[10px] font-semibold uppercase tracking-wide px-2 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-100">
											{#if coffee.roastery_url}
												<button onclick={refreshCoffee} disabled={refreshing} class="hover:text-blue-900 disabled:opacity-50" title={refreshing ? $t('detail.refreshing') : $t('detail.refresh')}>
													<svg viewBox="0 0 20 20" fill="currentColor" class="w-3 h-3 {refreshing ? 'animate-spin' : ''}"><path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd" /></svg>
												</button>
											{/if}
											{$t('detail.in_store')}
										</span>
									{:else}
										<span class="text-[10px] font-semibold uppercase tracking-wide px-2 py-0.5 rounded-full bg-stone-100 text-stone-400 border border-stone-200">{$t('detail.sold_out')}</span>
									{/if}
									{#if coffee.price != null}
										<span class="text-base font-bold text-stone-700">{coffee.price_wholesale != null ? coffee.price_wholesale : coffee.price}₴
											{#if coffee.price_wholesale != null}<span class="text-[10px] text-stone-300 line-through font-normal ml-0.5">{coffee.price}₴</span>{/if}
										</span>
									{/if}
								</div>
								<div class="flex items-center gap-1">
									<button onclick={async () => { if (coffee && coffee.in_stock) { await api.coffees.update(coffeeId, { in_stock: false }); await loadData(); onUpdated(); } }}
										class="w-5 h-5 rounded flex items-center justify-center text-xs font-bold
											{coffee.in_stock ? 'bg-stone-100 text-stone-500 hover:bg-stone-200' : 'bg-stone-50 text-stone-300 cursor-not-allowed'}"
										disabled={!coffee.in_stock}>−</button>
									<span class="text-base font-bold text-amber-700 w-4 text-center tabular-nums">{coffee.in_stock ? 1 : 0}</span>
									<button onclick={async () => { if (coffee && !coffee.in_stock) { await api.coffees.update(coffeeId, { in_stock: true }); await loadData(); onUpdated(); } }}
										class="w-5 h-5 rounded flex items-center justify-center text-xs font-bold
											bg-amber-50 text-amber-700 hover:bg-amber-100 border border-amber-200">+</button>
									<span class="text-[10px] text-stone-400 ml-0.5">{$t('detail.in_stock')}</span>
								</div>
							</div>
						</div>
						{#if refreshError}<p class="text-xs text-red-500">{refreshError}</p>{/if}

						<!-- Row 2: [image] | [details+bars] | [stats+comment] -->
						<div class="detail-3col">
							<!-- Col 1: Image -->
							{#if coffee.image_url}
								<div class="detail-inline-image">
									<img src={coffee.image_url} alt={coffee.name} class="w-full h-full object-contain" />
								</div>
							{/if}

							<!-- Col 2: Roastery, score, process, roast, taste bars, descriptors -->
							<div class="space-y-1.5 min-w-0">
								<a href={coffee.roastery_url ?? '#'} target={coffee.roastery_url ? '_blank' : undefined} rel="noopener"
									class="text-sm block {coffee.roastery_url ? 'text-amber-600 hover:text-amber-800' : 'text-stone-400 cursor-default'}">
									{coffee.roastery_ref?.name}
								</a>
								<div class="flex flex-wrap gap-x-5 gap-y-0.5 text-sm">
									{#if coffee.score != null}
										<div><span class="text-stone-400 text-[10px] uppercase tracking-wide">{$t('detail.score')}</span><p class="text-amber-700 font-bold text-sm">{coffee.score}</p></div>
									{/if}
									{#if coffee.process}
										<div><span class="text-stone-400 text-[10px] uppercase tracking-wide">{$t('detail.process')}</span><p class="text-stone-700 font-medium text-sm">{coffee.process}</p></div>
									{/if}
									{#if coffee.roast_level}
										<div><span class="text-stone-400 text-[10px] uppercase tracking-wide">{$t('detail.roast')}</span><p class="text-stone-700 font-medium text-sm">{coffee.roast_level}</p></div>
									{/if}
								</div>
								{#if coffee.sweetness != null || coffee.acidity != null || coffee.bitterness != null}
									<div class="space-y-1">
										{#if coffee.sweetness != null}
											<div class="flex items-center gap-2">
												<span class="text-[10px] text-stone-400 uppercase tracking-wide w-12">{$t('card.sweet')}</span>
												<div class="w-20 h-1.5 bg-card-inset rounded-full overflow-hidden"><div class="h-full rounded-full" style="width: {coffee.sweetness * 10}%; background: linear-gradient(90deg, #d4a574, #b45309);"></div></div>
												<span class="text-xs font-bold text-amber-800 w-4 text-right">{coffee.sweetness}</span>
											</div>
										{/if}
										{#if coffee.acidity != null}
											<div class="flex items-center gap-2">
												<span class="text-[10px] text-stone-400 uppercase tracking-wide w-12">{$t('card.acid')}</span>
												<div class="w-20 h-1.5 bg-card-inset rounded-full overflow-hidden"><div class="h-full rounded-full" style="width: {coffee.acidity * 10}%; background: linear-gradient(90deg, #d4a574, #b45309);"></div></div>
												<span class="text-xs font-bold text-amber-800 w-4 text-right">{coffee.acidity}</span>
											</div>
										{/if}
										{#if coffee.bitterness != null}
											<div class="flex items-center gap-2">
												<span class="text-[10px] text-stone-400 uppercase tracking-wide w-12">{$t('card.bitter')}</span>
												<div class="w-20 h-1.5 bg-card-inset rounded-full overflow-hidden"><div class="h-full rounded-full" style="width: {coffee.bitterness * 10}%; background: linear-gradient(90deg, #d4a574, #b45309);"></div></div>
												<span class="text-xs font-bold text-amber-800 w-4 text-right">{coffee.bitterness}</span>
											</div>
										{/if}
									</div>
								{/if}
							</div>

							<!-- Col 3: Comment + descriptors -->
							<div class="detail-right-col">
								{#if roasterCommentText || coffee.notes}
									<div class="bg-card-inset rounded-lg px-3 py-2 text-left w-full max-w-sm">
										{#if roasterCommentText}
											<p class="text-xs text-stone-400 uppercase tracking-wide mb-1">{$t('detail.notes')}</p>
											<p class="text-sm text-stone-600 italic leading-relaxed">{roasterCommentText}</p>
										{/if}
										{#if coffee.notes}
											<p class="text-xs text-stone-400 italic mt-1">{coffee.notes}</p>
										{/if}
									</div>
								{/if}
								{#if coffee.roastery_descriptors.length > 0}
									<div class="flex flex-wrap gap-1 mt-auto pt-1 justify-end">
										{#each coffee.roastery_descriptors as desc}
											<span class="px-2 py-0.5 rounded-full text-xs bg-amber-50 text-amber-700 border border-amber-100">{desc.name}</span>
										{/each}
									</div>
								{/if}
							</div>
						</div>
					{/if}
				</div>
			</div>

		<!-- Grinder + Reviews row -->
		<div class="detail-bottom-grid">
			<!-- Grinder Settings -->
			<div class="bg-card rounded-xl border border-stone-100 shadow-sm animate-card p-3 md:p-4 lg:p-6">
				<div class="flex items-center justify-between mb-3">
					<div class="flex items-center gap-2">
						<img src="/img/burr-icon.png" alt="" class="w-12 h-12 opacity-60" />
						<h3 class="font-semibold text-base text-stone-700">{$t('grinder.title')}</h3>
					</div>
					{#if currentGrinderId && currentBrewSetupId && !showSettingForm}
						{#if activeGrindSetting}
							<button onclick={() => { settingValue = String(activeGrindSetting.setting); settingNotes = activeGrindSetting.notes ?? ''; showSettingForm = true; }}
								class="text-sm text-amber-600 hover:text-amber-700 transition-colors">{$t('common.edit')}</button>
						{:else}
							<button onclick={() => { settingValue = ''; settingNotes = ''; showSettingForm = true; }}
								class="text-sm text-amber-600 hover:text-amber-700 transition-colors">+ {$t('tasting.add_short')}</button>
						{/if}
					{/if}
				</div>
				{#if coffee.grinder_settings.length === 0 && !showSettingForm}
					<div class="text-center py-2">
						<img src="/img/empty-grinder-new.png" alt="" class="mx-auto opacity-60" style="max-width: 100px;" />
						<p class="text-sm text-stone-500 mt-1">{$t('grinder.no_setting')}</p>
					</div>
				{/if}
				{#each coffee.grinder_settings as setting}
					<div class="detail-data-row">
						<span class="text-sm text-stone-600 truncate">{setting.grinder.manufacturer}{setting.grinder.model ? ` ${setting.grinder.model}` : ''}</span>
						<span class="text-sm text-stone-400 truncate">{setting.brew_setup.manufacturer}{setting.brew_setup.model ? ` ${setting.brew_setup.model}` : ''}</span>
						<GrindValue value={setting.setting} step={setting.grinder.step} class="text-2xl text-amber-700" />
					</div>
				{/each}
				{#if showSettingForm}
					<div class="mt-3 bg-card-inset rounded-xl p-4 space-y-3">
						<div class="flex items-center justify-center gap-3">
							<img src="/img/burr-icon.png" alt="" class="w-8 h-8 opacity-40" />
							<input type="number"
								step={currentGrinderObj?.step ?? 1}
								min={currentGrinderObj?.range_min ?? 0}
								max={currentGrinderObj?.range_max ?? undefined}
								bind:value={settingValue}
								placeholder={currentGrinderObj && currentGrinderObj.step % 1 !== 0 ? '12.5' : '12'}
								class="w-24 px-3 py-2 rounded-xl border border-stone-200 text-2xl font-bold text-amber-700 text-center bg-card
									focus:outline-none focus:ring-2 focus:ring-amber-400/50 tabular-nums" />
						</div>
						<input type="text" bind:value={settingNotes} placeholder={$t('grinder.notes')}
							class="w-full px-4 py-2.5 rounded-xl border border-stone-100 text-sm bg-card
								focus:outline-none focus:ring-2 focus:ring-amber-400/50 placeholder:text-stone-300" />
						<div class="flex items-center justify-between">
							{#if activeGrindSetting}
								<button onclick={() => { deleteGrinderSetting(activeGrindSetting.id); showSettingForm = false; }}
									class="text-sm text-red-400 hover:text-red-600 transition-colors">{$t('detail.delete')}</button>
							{:else}
								<div></div>
							{/if}
							<div class="flex gap-2">
								<button onclick={() => showSettingForm = false} class="px-4 py-2 text-stone-400 text-sm">{$t('grinder.cancel')}</button>
								<button onclick={addGrinderSetting}
									class="px-5 py-2 bg-amber-700 text-white rounded-lg text-sm hover:bg-amber-800">{$t('grinder.save')}</button>
							</div>
						</div>
					</div>
				{/if}
			</div>

			<!-- Reviews -->
			<div class="bg-card rounded-xl border border-stone-100 shadow-sm animate-card p-3 md:p-4 lg:p-6">
				<div class="flex items-center justify-between mb-3">
					<div class="flex items-center gap-2">
						<img src="/img/coffee-cup.png" alt="" class="w-12 h-12 opacity-60" />
						<h3 class="font-semibold text-base text-stone-700">{$t('tasting.title')}</h3>
					</div>
					{#if currentPersonId && currentBrewSetupId && editingReviewTasterId === null}
						{#if activeReview}
							<button onclick={() => startReview(currentPersonId!, currentBrewSetupId!, activeReview)}
								class="text-sm text-amber-600 hover:text-amber-700 transition-colors">{$t('common.edit')}</button>
						{:else}
							<button onclick={() => startReview(currentPersonId!)}
								class="text-sm text-amber-600 hover:text-amber-700 transition-colors">+ {$t('tasting.add_short')}</button>
						{/if}
					{/if}
				</div>

				{#if coffee.reviews.length === 0 && editingReviewTasterId === null}
					<div class="text-center py-2">
						<img src="/img/no-reviews.png" alt="" class="mx-auto opacity-70" style="max-width: 100px;" />
						<p class="text-sm text-stone-500 mt-1">{$t('tasting.empty')}</p>
					</div>
				{/if}

				{#if editingReviewTasterId}
					<ReviewForm
						tasterName={tasters.find(ta => ta.id === editingReviewTasterId)?.name ?? ''}
						brewSetups={brewSetupsList}
						bind:brewSetupId={reviewBrewSetupId}
						bind:rating={reviewRating}
						bind:comment={reviewComment}
						bind:descriptorIds={reviewDescriptors}
						{descriptors}
						{suggestedDescriptorIds}
						onSave={saveReview}
						onCancel={cancelReview}
						onDelete={activeReview ? () => { deleteReview(activeReview.id); cancelReview(); } : undefined}
					/>
				{:else}
					{#each coffee.reviews as review}
						<div class="detail-data-row">
							<span class="text-sm text-stone-600 truncate">{review.taster.name}</span>
							<span class="text-sm text-stone-400 truncate">{review.brew_setup.manufacturer}{review.brew_setup.model ? ` ${review.brew_setup.model}` : ''}</span>
							<span class="text-2xl font-bold text-amber-700 tabular-nums">{review.rating}</span>
						</div>
					{/each}
				{/if}
			</div>

		</div>
	</div>
{/if}

<style>
	/* Page container */
	.detail-page {
		max-width: 72rem;
		margin: 0 auto;
		padding: 0.5rem 0.5rem;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	@media (min-width: 768px) {
		.detail-page {
			padding: 0.5rem 1rem;
			gap: 0.6rem;
		}
	}

	@media (min-width: 1280px) {
		.detail-page {
			padding: 1.5rem 2.5rem;
			gap: 1rem;
		}
	}

	/* 3-column layout: image | details | comment */
	.detail-3col {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
	}

	@media (min-width: 768px) {
		.detail-3col {
			flex-wrap: nowrap;
			gap: 0.75rem;
		}
	}

	.detail-inline-image {
		width: 80px;
		flex-shrink: 0;
		display: flex;
		align-items: flex-start;
		justify-content: center;
	}

	@media (min-width: 768px) {
		.detail-inline-image {
			width: 100px;
		}
	}

	.detail-right-col {
		width: 100%;
		display: flex;
		flex-direction: column;
		align-items: flex-start;
	}

	@media (min-width: 768px) {
		.detail-right-col {
			width: auto;
			flex: 1;
			align-items: flex-end;
			min-width: 120px;
		}
	}

	@media (min-width: 1024px) {
		.detail-inline-image { width: 130px; }
	}

	@media (min-width: 1280px) {
		.detail-3col { gap: 1.5rem; }
		.detail-inline-image { width: 200px; }
	}

	.detail-header-grid {
		display: grid;
		grid-template-columns: 1fr auto;
		align-items: start;
		gap: 0.5rem;
	}

	.detail-bottom-grid {
		display: grid;
		grid-template-columns: 1fr;
		gap: 0.5rem;
	}

	@media (min-width: 768px) {
		.detail-bottom-grid {
			grid-template-columns: 1fr 1fr;
		}
	}

	@media (min-width: 1280px) {
		.detail-bottom-grid { gap: 1rem; }
	}

	.detail-data-row {
		display: grid;
		grid-template-columns: 35% 40% auto;
		align-items: center;
		gap: 0.5rem;
		padding: 0.35rem 0;
		border-bottom: 1px solid rgba(0,0,0,0.03);
	}

	.detail-data-row:last-child {
		border-bottom: none;
	}
</style>
