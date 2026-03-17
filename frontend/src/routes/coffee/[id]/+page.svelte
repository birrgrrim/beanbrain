<script lang="ts">
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import { api, type Coffee, type Descriptor, type Equipment, type BrewMethod, type Taster, type BasketSize } from '$lib/api';
	import StarRating from '$lib/components/StarRating.svelte';
	import DescriptorPicker from '$lib/components/DescriptorPicker.svelte';

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

	const coffeeId = $derived(Number(page.params.id));

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

	// Pre-suggest roastery descriptors in tasting form
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
		goto('/');
	}
</script>

{#if loading}
	<div class="text-center py-12 text-stone-400">Loading...</div>
{:else if coffee}
	<div class="max-w-2xl mx-auto space-y-6">
		<!-- Header -->
		<div class="flex items-start justify-between gap-3">
			<div>
				<a href="/" class="text-sm text-stone-400 hover:text-stone-600 transition-colors">&larr; Back</a>
				<h1 class="text-2xl font-bold text-stone-800 mt-1">{coffee.name}</h1>
				<p class="text-stone-500">{coffee.roastery}</p>
			</div>
			<button
				onclick={deleteCoffee}
				class="text-sm text-red-400 hover:text-red-600 transition-colors mt-2"
			>
				Delete
			</button>
		</div>

		<!-- Details card -->
		<div class="bg-white rounded-xl border border-stone-200 p-5 space-y-3">
			{#if coffee.image_url}
				<div class="flex justify-center">
					<img src={coffee.image_url} alt={coffee.name} class="h-40 rounded-lg object-contain" />
				</div>
			{/if}

			<div class="flex flex-wrap gap-x-6 gap-y-1 text-sm">
				{#if coffee.origin}
					<div><span class="text-stone-400">Origin:</span> <span class="text-stone-700">{coffee.origin}</span></div>
				{/if}
				{#if coffee.process}
					<div><span class="text-stone-400">Process:</span> <span class="text-stone-700">{coffee.process}</span></div>
				{/if}
				{#if coffee.roast_level}
					<div><span class="text-stone-400">Roast:</span> <span class="text-stone-700">{coffee.roast_level}</span></div>
				{/if}
			</div>

			{#if coffee.score || coffee.sweetness || coffee.acidity || coffee.bitterness}
				<div class="flex flex-wrap gap-4 p-3 bg-stone-50 rounded-lg text-center">
					{#if coffee.score}
						<div>
							<p class="text-xs text-stone-400">Score</p>
							<p class="text-lg font-bold text-amber-700">{coffee.score}</p>
						</div>
					{/if}
					{#if coffee.sweetness}
						<div>
							<p class="text-xs text-stone-400">Sweetness</p>
							<p class="text-sm font-medium">{coffee.sweetness}</p>
						</div>
					{/if}
					{#if coffee.acidity}
						<div>
							<p class="text-xs text-stone-400">Acidity</p>
							<p class="text-sm font-medium">{coffee.acidity}</p>
						</div>
					{/if}
					{#if coffee.bitterness}
						<div>
							<p class="text-xs text-stone-400">Bitterness</p>
							<p class="text-sm font-medium">{coffee.bitterness}</p>
						</div>
					{/if}
				</div>
			{/if}

			{#if coffee.roastery_url}
				<a href={coffee.roastery_url} target="_blank" rel="noopener"
					class="text-sm text-amber-700 hover:text-amber-900 underline"
				>View on roastery site</a>
			{/if}

			{#if coffee.notes}
				<p class="text-sm text-stone-600 italic">{coffee.notes}</p>
			{/if}

			{#if coffee.roastery_descriptors.length > 0}
				<div>
					<p class="text-xs text-stone-400 mb-1">Roastery says:</p>
					<div class="flex flex-wrap gap-1">
						{#each coffee.roastery_descriptors as desc}
							<span class="px-2 py-0.5 rounded-full text-xs bg-amber-50 text-amber-700 border border-amber-200">
								{desc.name}
							</span>
						{/each}
					</div>
				</div>
			{/if}
		</div>

		<!-- Grinder Settings -->
		<div class="bg-white rounded-xl border border-stone-200 p-5">
			<div class="flex items-center justify-between mb-3">
				<h2 class="font-semibold text-stone-800">Grinder Setting</h2>
				{#if !showSettingForm}
					<button
						onclick={() => showSettingForm = true}
						class="text-sm text-amber-700 hover:text-amber-900 transition-colors"
					>+ Add</button>
				{/if}
			</div>

			{#if coffee.grinder_settings.length === 0 && !showSettingForm}
				<p class="text-sm text-stone-400">No grinder setting recorded yet</p>
			{/if}

			{#each coffee.grinder_settings as setting}
				<div class="flex items-center justify-between py-2 border-b border-stone-100 last:border-0">
					<div>
						<span class="text-2xl font-bold text-amber-700">{setting.setting}</span>
						<span class="text-sm text-stone-400 ml-2">
							{setting.equipment.name} / {setting.brew_method.name}
							{#if setting.basket_size}
								/ {setting.basket_size.label}
							{/if}
						</span>
						{#if setting.notes}
							<p class="text-xs text-stone-400 mt-0.5">{setting.notes}</p>
						{/if}
					</div>
					<button
						onclick={() => deleteGrinderSetting(setting.id)}
						class="text-xs text-red-400 hover:text-red-600 transition-colors"
					>&times;</button>
				</div>
			{/each}

			{#if showSettingForm}
				<div class="mt-3 p-3 bg-stone-50 rounded-lg space-y-3">
					<div class="flex gap-3">
						<div class="flex-1">
							<label for="setting" class="block text-xs text-stone-500 mb-1">Setting</label>
							<input
								id="setting" type="number" step="0.5" bind:value={settingValue}
								class="w-full px-3 py-1.5 rounded border border-stone-300 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
								placeholder="12.5"
							/>
						</div>
						<div class="flex-1">
							<label for="basket" class="block text-xs text-stone-500 mb-1">Basket</label>
							<select
								id="basket"
								bind:value={settingBasketId}
								class="w-full px-3 py-1.5 rounded border border-stone-300 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500 bg-white"
							>
								<option value={null}>—</option>
								{#each basketSizes as bs}
									<option value={bs.id}>{bs.label}</option>
								{/each}
							</select>
						</div>
						<div class="flex-1">
							<label for="setting_notes" class="block text-xs text-stone-500 mb-1">Notes</label>
							<input
								id="setting_notes" type="text" bind:value={settingNotes}
								class="w-full px-3 py-1.5 rounded border border-stone-300 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
								placeholder="Optional"
							/>
						</div>
					</div>
					<div class="flex gap-2">
						<button onclick={addGrinderSetting}
							class="px-4 py-1.5 bg-amber-700 text-white rounded text-sm hover:bg-amber-800 transition-colors"
						>Save</button>
						<button onclick={() => showSettingForm = false}
							class="px-4 py-1.5 text-stone-500 text-sm hover:text-stone-700 transition-colors"
						>Cancel</button>
					</div>
				</div>
			{/if}
		</div>

		<!-- Tastings -->
		<div class="bg-white rounded-xl border border-stone-200 p-5">
			<div class="flex items-center justify-between mb-3">
				<h2 class="font-semibold text-stone-800">Tastings</h2>
				{#if !showTastingForm}
					<button
						onclick={() => showTastingForm = true}
						class="text-sm text-amber-700 hover:text-amber-900 transition-colors"
					>+ Add Tasting</button>
				{/if}
			</div>

			{#if coffee.tastings.length === 0 && !showTastingForm}
				<p class="text-sm text-stone-400">No tastings yet — be the first to rate!</p>
			{/if}

			{#each coffee.tastings as tasting}
				<div class="py-3 border-b border-stone-100 last:border-0">
					<div class="flex items-center justify-between">
						<div class="flex items-center gap-3">
							<span class="font-medium text-stone-700">{tasting.taster.name}</span>
							<StarRating rating={tasting.rating} />
							<span class="text-xs text-stone-400">{tasting.rating}/10</span>
						</div>
						<button
							onclick={() => deleteTasting(tasting.id)}
							class="text-xs text-red-400 hover:text-red-600 transition-colors"
						>&times;</button>
					</div>
					{#if tasting.comment}
						<p class="text-sm text-stone-600 mt-1">{tasting.comment}</p>
					{/if}
					{#if tasting.descriptors.length > 0}
						<div class="flex flex-wrap gap-1 mt-1.5">
							{#each tasting.descriptors as desc}
								<span class="px-2 py-0.5 rounded-full text-xs bg-stone-100 text-stone-600">
									{desc.name}
								</span>
							{/each}
						</div>
					{/if}
					<p class="text-xs text-stone-300 mt-1">
						{new Date(tasting.tasted_at).toLocaleDateString()}
					</p>
				</div>
			{/each}

			{#if showTastingForm}
				<div class="mt-3 p-4 bg-stone-50 rounded-lg space-y-3">
					<div>
						<label for="taster" class="block text-xs text-stone-500 mb-1">Who's tasting?</label>
						{#if tasters.length > 0}
							<div class="flex gap-2">
								<select
									id="taster"
									bind:value={tastingTasterId}
									class="flex-1 px-3 py-1.5 rounded border border-stone-300 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500 bg-white"
								>
									<option value={null}>Select or add new...</option>
									{#each tasters as t}
										<option value={t.id}>{t.name}</option>
									{/each}
								</select>
								{#if !tastingTasterId}
									<input
										type="text"
										bind:value={newTasterName}
										placeholder="New name"
										class="flex-1 px-3 py-1.5 rounded border border-stone-300 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
									/>
								{/if}
							</div>
						{:else}
							<input
								type="text"
								bind:value={newTasterName}
								placeholder="Your name"
								class="w-full px-3 py-1.5 rounded border border-stone-300 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
							/>
						{/if}
					</div>

					<div>
						<span class="block text-xs text-stone-500 mb-1">Rating</span>
						<div class="flex items-center gap-2">
							<StarRating rating={tastingRating} interactive onRate={(v) => tastingRating = v} />
							{#if tastingRating > 0}
								<span class="text-sm text-stone-500">{tastingRating}/10</span>
							{/if}
						</div>
					</div>

					<div>
						<label for="comment" class="block text-xs text-stone-500 mb-1">Comment</label>
						<textarea
							id="comment" bind:value={tastingComment} rows={2}
							class="w-full px-3 py-1.5 rounded border border-stone-300 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500 resize-none"
							placeholder="What did you taste?"
						></textarea>
					</div>

					<div>
						<p class="text-xs text-stone-500 mb-1">What you taste</p>
						{#if suggestedDescriptorIds.length > 0}
							<p class="text-xs text-amber-600 mb-1">Roastery suggests:</p>
							<div class="flex flex-wrap gap-1 mb-2">
								{#each suggestedDescriptorIds as id}
									{@const desc = descriptors.find(d => d.id === id)}
									{@const isSelected = tastingDescriptors.includes(id)}
									{#if desc}
										<button
											type="button"
											class="px-2 py-0.5 rounded-full text-xs transition-colors
												{isSelected
													? 'bg-amber-600 text-white'
													: 'bg-amber-100 text-amber-700 hover:bg-amber-200'}"
											onclick={() => toggleTastingDescriptor(id)}
										>
											{desc.name}
										</button>
									{/if}
								{/each}
							</div>
						{/if}
						<DescriptorPicker {descriptors} selected={tastingDescriptors} onToggle={toggleTastingDescriptor} />
					</div>

					<div class="flex gap-2">
						<button
							onclick={addTasting}
							disabled={(!tastingTasterId && !newTasterName.trim()) || tastingRating === 0}
							class="px-4 py-1.5 bg-amber-700 text-white rounded text-sm hover:bg-amber-800 transition-colors
								disabled:opacity-50 disabled:cursor-not-allowed"
						>Save Tasting</button>
						<button
							onclick={() => { showTastingForm = false; tastingRating = 0; tastingDescriptors = []; }}
							class="px-4 py-1.5 text-stone-500 text-sm hover:text-stone-700 transition-colors"
						>Cancel</button>
					</div>
				</div>
			{/if}
		</div>
	</div>
{/if}
