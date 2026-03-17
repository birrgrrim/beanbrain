<script lang="ts">
	import { api, type Coffee, type Descriptor, type Equipment, type BrewMethod, type Taster, type BasketSize } from '$lib/api';
	import StarRating from './StarRating.svelte';
	import DescriptorAutocomplete from './DescriptorAutocomplete.svelte';
	import Icons from './Icons.svelte';

	let { coffeeId, onDeleted }: {
		coffeeId: number;
		onDeleted: () => void;
	} = $props();

	let coffee = $state<Coffee | null>(null);
	let descriptors = $state<Descriptor[]>([]);
	let equipmentList = $state<Equipment[]>([]);
	let brewMethods = $state<BrewMethod[]>([]);
	let tasters = $state<Taster[]>([]);
	let basketSizes = $state<BasketSize[]>([]);
	let loading = $state(true);

	// Tasting form
	let showTastingForm = $state(false);
	let tastingTasterId = $state<number | null>(null);
	let newTasterName = $state('');
	let tastingRating = $state(0);
	let tastingComment = $state('');
	let tastingDescriptors = $state<number[]>([]);

	// Grinder setting form
	let showSettingForm = $state(false);
	let settingValue = $state('');
	let settingNotes = $state('');
	let settingBasketId = $state<number | null>(null);

	async function loadData() {
		loading = true;
		const [c, d, eq, bm, t, bs] = await Promise.all([
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
		tasters = t;
		basketSizes = bs;
		loading = false;
	}

	$effect(() => {
		coffeeId;
		loadData();
	});

	const suggestedDescriptorIds = $derived(
		coffee?.roastery_descriptors.map(d => d.id) ?? []
	);

	function toggleTastingDescriptor(id: number) {
		if (tastingDescriptors.includes(id)) {
			tastingDescriptors = tastingDescriptors.filter(d => d !== id);
		} else {
			tastingDescriptors = [...tastingDescriptors, id];
		}
	}

	async function addTasting() {
		let tId = tastingTasterId;
		if (!tId && newTasterName.trim()) {
			const newTaster = await api.tasters.create(newTasterName.trim());
			tId = newTaster.id;
		}
		if (!tId || tastingRating === 0) return;

		await api.tastings.create(coffeeId, {
			taster_id: tId,
			rating: tastingRating,
			comment: tastingComment.trim() || undefined,
			descriptor_ids: tastingDescriptors.length > 0 ? tastingDescriptors : undefined,
		});
		tastingTasterId = null;
		newTasterName = '';
		tastingRating = 0;
		tastingComment = '';
		tastingDescriptors = [];
		showTastingForm = false;
		await loadData();
	}

	async function deleteTasting(tastingId: number) {
		await api.tastings.delete(coffeeId, tastingId);
		await loadData();
	}

	async function addGrinderSetting() {
		const grinder = equipmentList.find(e => e.type === 'grinder');
		const espresso = brewMethods.find(m => m.name === 'Espresso');
		if (!grinder || !espresso || !settingValue) return;

		await api.grinderSettings.create(coffeeId, {
			equipment_id: grinder.id,
			brew_method_id: espresso.id,
			basket_size_id: settingBasketId ?? undefined,
			setting: parseFloat(settingValue),
			notes: settingNotes.trim() || undefined,
		});
		settingValue = '';
		settingNotes = '';
		settingBasketId = null;
		showSettingForm = false;
		await loadData();
	}

	async function deleteGrinderSetting(settingId: number) {
		await api.grinderSettings.delete(coffeeId, settingId);
		await loadData();
	}

	async function deleteCoffee() {
		if (!confirm('Delete this coffee and all its tastings?')) return;
		await api.coffees.delete(coffeeId);
		onDeleted();
	}
</script>

{#if loading}
	<div class="flex items-center justify-center h-full">
		<div class="text-stone-300">Loading...</div>
	</div>
{:else if coffee}
	<div class="max-w-2xl mx-auto p-6 space-y-6">
		<!-- Header -->
		<div class="flex items-start justify-between">
			<div>
				<h2 class="text-2xl font-bold text-stone-800" style="font-family: 'DM Serif Display', serif;">
					{coffee.name}
				</h2>
				<p class="text-stone-400 text-sm mt-0.5">{coffee.roastery}</p>
			</div>
			<button onclick={deleteCoffee} class="p-2 text-stone-300 hover:text-red-500 transition-colors" title="Delete coffee">
				<Icons icon="delete" size={18} />
			</button>
		</div>

		<!-- Info card -->
		<div class="bg-white rounded-2xl border border-stone-100 shadow-sm overflow-hidden">
			{#if coffee.image_url}
				<div class="bg-stone-50 p-6 flex justify-center border-b border-stone-100">
					<img src={coffee.image_url} alt={coffee.name} class="h-44 object-contain" />
				</div>
			{/if}

			<div class="p-5 space-y-4">
				<div class="flex flex-wrap gap-x-8 gap-y-2 text-sm">
					{#if coffee.origin}
						<div>
							<span class="text-stone-300 text-xs uppercase tracking-wide">Origin</span>
							<p class="text-stone-700 font-medium">{coffee.origin}</p>
						</div>
					{/if}
					{#if coffee.process}
						<div>
							<span class="text-stone-300 text-xs uppercase tracking-wide">Process</span>
							<p class="text-stone-700 font-medium">{coffee.process}</p>
						</div>
					{/if}
					{#if coffee.roast_level}
						<div>
							<span class="text-stone-300 text-xs uppercase tracking-wide">Roast</span>
							<p class="text-stone-700 font-medium">{coffee.roast_level}</p>
						</div>
					{/if}
				</div>

				{#if coffee.score || coffee.sweetness || coffee.acidity || coffee.bitterness}
					<div class="flex gap-6 py-3 px-4 bg-stone-50 rounded-xl">
						{#if coffee.score}
							<div class="text-center">
								<p class="text-2xl font-bold text-amber-700">{coffee.score}</p>
								<p class="text-[10px] text-stone-300 uppercase tracking-wide">Score</p>
							</div>
						{/if}
						{#if coffee.sweetness}
							<div class="text-center">
								<p class="text-sm font-semibold text-stone-600">{coffee.sweetness}</p>
								<p class="text-[10px] text-stone-300 uppercase tracking-wide">Sweet</p>
							</div>
						{/if}
						{#if coffee.acidity}
							<div class="text-center">
								<p class="text-sm font-semibold text-stone-600">{coffee.acidity}</p>
								<p class="text-[10px] text-stone-300 uppercase tracking-wide">Acid</p>
							</div>
						{/if}
						{#if coffee.bitterness}
							<div class="text-center">
								<p class="text-sm font-semibold text-stone-600">{coffee.bitterness}</p>
								<p class="text-[10px] text-stone-300 uppercase tracking-wide">Bitter</p>
							</div>
						{/if}
					</div>
				{/if}

				{#if coffee.roastery_descriptors.length > 0}
					<div>
						<p class="text-[10px] text-stone-300 uppercase tracking-wide mb-1.5">Flavor profile</p>
						<div class="flex flex-wrap gap-1.5">
							{#each coffee.roastery_descriptors as desc}
								<span class="px-2.5 py-1 rounded-full text-xs bg-amber-50 text-amber-700 border border-amber-100">
									{desc.name}
								</span>
							{/each}
						</div>
					</div>
				{/if}

				{#if coffee.roastery_url}
					<a href={coffee.roastery_url} target="_blank" rel="noopener"
						class="inline-flex items-center gap-1.5 text-xs text-amber-600 hover:text-amber-800 transition-colors">
						<Icons icon="link" size={12} />
						View on roastery site
					</a>
				{/if}

				{#if coffee.notes}
					<p class="text-sm text-stone-500 italic">{coffee.notes}</p>
				{/if}
			</div>
		</div>

		<!-- Grinder Settings -->
		<div class="bg-white rounded-2xl border border-stone-100 shadow-sm p-5">
			<div class="flex items-center justify-between mb-4">
				<div class="flex items-center gap-2">
					<Icons icon="grinder" size={18} className="text-stone-400" />
					<h3 class="font-semibold text-stone-700">Grinder Setting</h3>
				</div>
				{#if !showSettingForm}
					<button onclick={() => showSettingForm = true}
						class="text-xs text-amber-600 hover:text-amber-800 transition-colors font-medium">+ Add</button>
				{/if}
			</div>

			{#if coffee.grinder_settings.length === 0 && !showSettingForm}
				<p class="text-sm text-stone-300">No setting recorded yet</p>
			{/if}

			{#each coffee.grinder_settings as setting}
				<div class="flex items-center justify-between py-3 border-b border-stone-50 last:border-0">
					<div class="flex items-center gap-4">
						<span class="text-3xl font-bold text-amber-700 tabular-nums">{setting.setting}</span>
						<div class="text-xs text-stone-400">
							<p>{setting.equipment.name}</p>
							<p>{setting.brew_method.name}{#if setting.basket_size} &middot; {setting.basket_size.label}{/if}</p>
							{#if setting.notes}<p class="text-stone-300 mt-0.5">{setting.notes}</p>{/if}
						</div>
					</div>
					<button onclick={() => deleteGrinderSetting(setting.id)}
						class="p-1 text-stone-200 hover:text-red-400 transition-colors">
						<Icons icon="delete" size={14} />
					</button>
				</div>
			{/each}

			{#if showSettingForm}
				<div class="mt-3 p-4 bg-stone-50 rounded-xl space-y-3">
					<div class="flex gap-3">
						<div class="flex-1">
							<label for="setting" class="block text-xs text-stone-400 mb-1">Setting</label>
							<input id="setting" type="number" step="0.5" bind:value={settingValue}
								class="w-full px-3 py-2 rounded-lg border border-stone-200 text-sm bg-white
									focus:outline-none focus:ring-2 focus:ring-amber-400/50" placeholder="12.5" />
						</div>
						<div class="flex-1">
							<label for="basket" class="block text-xs text-stone-400 mb-1">Basket</label>
							<select id="basket" bind:value={settingBasketId}
								class="w-full px-3 py-2 rounded-lg border border-stone-200 text-sm bg-white
									focus:outline-none focus:ring-2 focus:ring-amber-400/50">
								<option value={null}>—</option>
								{#each basketSizes as bs}<option value={bs.id}>{bs.label}</option>{/each}
							</select>
						</div>
						<div class="flex-1">
							<label for="sn" class="block text-xs text-stone-400 mb-1">Notes</label>
							<input id="sn" type="text" bind:value={settingNotes}
								class="w-full px-3 py-2 rounded-lg border border-stone-200 text-sm bg-white
									focus:outline-none focus:ring-2 focus:ring-amber-400/50" placeholder="Optional" />
						</div>
					</div>
					<div class="flex gap-2">
						<button onclick={addGrinderSetting}
							class="px-4 py-2 bg-amber-700 text-white rounded-lg text-sm hover:bg-amber-800 transition-colors">Save</button>
						<button onclick={() => showSettingForm = false}
							class="px-4 py-2 text-stone-400 text-sm hover:text-stone-600 transition-colors">Cancel</button>
					</div>
				</div>
			{/if}
		</div>

		<!-- Tastings -->
		<div class="bg-white rounded-2xl border border-stone-100 shadow-sm p-5">
			<div class="flex items-center justify-between mb-4">
				<div class="flex items-center gap-2">
					<Icons icon="cup" size={18} className="text-stone-400" />
					<h3 class="font-semibold text-stone-700">Tastings</h3>
				</div>
				{#if !showTastingForm}
					<button onclick={() => showTastingForm = true}
						class="text-xs text-amber-600 hover:text-amber-800 transition-colors font-medium">+ Add Tasting</button>
				{/if}
			</div>

			{#if coffee.tastings.length === 0 && !showTastingForm}
				<div class="text-center py-4">
					<Icons icon="cup" size={28} className="mx-auto text-stone-200 mb-1" />
					<p class="text-sm text-stone-300">No tastings yet</p>
				</div>
			{/if}

			{#each coffee.tastings as tasting}
				<div class="py-3 border-b border-stone-50 last:border-0">
					<div class="flex items-center justify-between">
						<div class="flex items-center gap-3">
							<span class="text-sm font-medium text-stone-700">{tasting.taster.name}</span>
							<StarRating rating={tasting.rating} />
							<span class="text-xs text-stone-300 tabular-nums">{tasting.rating}/10</span>
						</div>
						<button onclick={() => deleteTasting(tasting.id)}
							class="p-1 text-stone-200 hover:text-red-400 transition-colors">
							<Icons icon="delete" size={14} />
						</button>
					</div>
					{#if tasting.comment}
						<p class="text-sm text-stone-500 mt-1.5">{tasting.comment}</p>
					{/if}
					{#if tasting.descriptors.length > 0}
						<div class="flex flex-wrap gap-1 mt-2">
							{#each tasting.descriptors as desc}
								<span class="px-2 py-0.5 rounded-full text-xs bg-stone-50 text-stone-500 border border-stone-100">
									{desc.name}
								</span>
							{/each}
						</div>
					{/if}
					<p class="text-[10px] text-stone-200 mt-1.5">{new Date(tasting.tasted_at).toLocaleDateString()}</p>
				</div>
			{/each}

			{#if showTastingForm}
				<div class="mt-3 p-4 bg-stone-50 rounded-xl space-y-3">
					<div>
						<label for="taster" class="block text-xs text-stone-400 mb-1">Who's tasting?</label>
						{#if tasters.length > 0}
							<div class="flex gap-2">
								<select id="taster" bind:value={tastingTasterId}
									class="flex-1 px-3 py-2 rounded-lg border border-stone-200 text-sm bg-white
										focus:outline-none focus:ring-2 focus:ring-amber-400/50">
									<option value={null}>Select or add new...</option>
									{#each tasters as t}<option value={t.id}>{t.name}</option>{/each}
								</select>
								{#if !tastingTasterId}
									<input type="text" bind:value={newTasterName} placeholder="New name"
										class="flex-1 px-3 py-2 rounded-lg border border-stone-200 text-sm bg-white
											focus:outline-none focus:ring-2 focus:ring-amber-400/50" />
								{/if}
							</div>
						{:else}
							<input type="text" bind:value={newTasterName} placeholder="Your name"
								class="w-full px-3 py-2 rounded-lg border border-stone-200 text-sm bg-white
									focus:outline-none focus:ring-2 focus:ring-amber-400/50" />
						{/if}
					</div>

					<div>
						<span class="block text-xs text-stone-400 mb-1">Rating</span>
						<div class="flex items-center gap-2">
							<StarRating rating={tastingRating} interactive onRate={(v) => tastingRating = v} />
							{#if tastingRating > 0}
								<span class="text-sm text-stone-400 tabular-nums">{tastingRating}/10</span>
							{/if}
						</div>
					</div>

					<div>
						<label for="comment" class="block text-xs text-stone-400 mb-1">Comment</label>
						<textarea id="comment" bind:value={tastingComment} rows={2}
							class="w-full px-3 py-2 rounded-lg border border-stone-200 text-sm bg-white
								focus:outline-none focus:ring-2 focus:ring-amber-400/50 resize-none"
							placeholder="What did you taste?"></textarea>
					</div>

					<div>
						<p class="text-xs text-stone-400 mb-1">Flavors you taste</p>
						<DescriptorAutocomplete
							{descriptors}
							selected={tastingDescriptors}
							suggested={suggestedDescriptorIds}
							onToggle={toggleTastingDescriptor}
						/>
					</div>

					<div class="flex gap-2">
						<button onclick={addTasting}
							disabled={(!tastingTasterId && !newTasterName.trim()) || tastingRating === 0}
							class="px-4 py-2 bg-amber-700 text-white rounded-lg text-sm hover:bg-amber-800
								transition-colors disabled:opacity-50 disabled:cursor-not-allowed">Save Tasting</button>
						<button onclick={() => { showTastingForm = false; tastingRating = 0; tastingDescriptors = []; }}
							class="px-4 py-2 text-stone-400 text-sm hover:text-stone-600 transition-colors">Cancel</button>
					</div>
				</div>
			{/if}
		</div>
	</div>
{/if}
