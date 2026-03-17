<script lang="ts">
	import { api, type Descriptor, type ScrapeResult } from '$lib/api';
	import DescriptorAutocomplete from './DescriptorAutocomplete.svelte';
	import Icons from './Icons.svelte';

	let { onCreated, onCancel }: {
		onCreated: (id: number) => void;
		onCancel: () => void;
	} = $props();

	let scrapeUrl = $state('');
	let scraping = $state(false);
	let scrapeError = $state('');
	let scraped = $state<ScrapeResult | null>(null);

	let name = $state('');
	let roastery = $state('');
	let origin = $state('');
	let process = $state('');
	let roastLevel = $state('');
	let roasteryUrl = $state('');
	let imageUrl = $state('');
	let score = $state<number | undefined>();
	let sweetness = $state('');
	let acidity = $state('');
	let bitterness = $state('');
	let notes = $state('');
	let selectedDescriptors = $state<number[]>([]);
	let descriptors = $state<Descriptor[]>([]);
	let saving = $state(false);

	$effect(() => {
		api.descriptors.list().then(d => descriptors = d);
	});

	async function handleScrape() {
		if (!scrapeUrl.trim()) return;
		scraping = true;
		scrapeError = '';
		try {
			const result = await api.scrape(scrapeUrl.trim());
			scraped = result;
			name = result.name || '';
			roastery = result.roastery || '';
			origin = result.origin || '';
			process = result.process || '';
			roastLevel = result.roast_level || '';
			roasteryUrl = result.roastery_url || '';
			imageUrl = result.image_url || '';
			score = result.score ?? undefined;
			sweetness = result.sweetness || '';
			acidity = result.acidity || '';
			bitterness = result.bitterness || '';

			const enDescriptors = result.flavor_descriptors?.en || [];
			const matched: number[] = [];
			for (const flavorName of enDescriptors) {
				const found = descriptors.find(d => d.name.toLowerCase() === flavorName.toLowerCase());
				if (found) matched.push(found.id);
			}
			selectedDescriptors = matched;
		} catch (e) {
			scrapeError = e instanceof Error ? e.message : 'Failed to scrape';
		}
		scraping = false;
	}

	function toggleDescriptor(id: number) {
		if (selectedDescriptors.includes(id)) {
			selectedDescriptors = selectedDescriptors.filter(d => d !== id);
		} else {
			selectedDescriptors = [...selectedDescriptors, id];
		}
	}

	async function handleSubmit(e: Event) {
		e.preventDefault();
		if (!name.trim() || !roastery.trim()) return;

		saving = true;
		const coffee = await api.coffees.create({
			name: name.trim(),
			roastery: roastery.trim(),
			origin: origin.trim() || undefined,
			process: process.trim() || undefined,
			roast_level: roastLevel.trim() || undefined,
			roastery_url: roasteryUrl.trim() || undefined,
			image_url: imageUrl.trim() || undefined,
			score,
			sweetness: sweetness.trim() || undefined,
			acidity: acidity.trim() || undefined,
			bitterness: bitterness.trim() || undefined,
			notes: notes.trim() || undefined,
			roastery_descriptor_ids: selectedDescriptors.length > 0 ? selectedDescriptors : undefined,
		});
		onCreated(coffee.id);
	}
</script>

<div class="max-w-2xl mx-auto p-6 space-y-6">
	<div class="flex items-center justify-between">
		<h2 class="text-2xl font-bold text-stone-800" style="font-family: 'DM Serif Display', serif;">
			Add Coffee
		</h2>
		<button onclick={onCancel} class="p-2 text-stone-300 hover:text-stone-500 transition-colors">
			<Icons icon="back" size={18} />
		</button>
	</div>

	<!-- URL Auto-fill -->
	<div class="bg-amber-50/50 rounded-2xl border border-amber-100 p-4">
		<div class="flex items-center gap-2 mb-2">
			<Icons icon="link" size={14} className="text-amber-500" />
			<p class="text-sm font-medium text-amber-700">Paste a roastery URL to auto-fill</p>
		</div>
		<div class="flex gap-2">
			<input type="url" bind:value={scrapeUrl}
				placeholder="https://madheadscoffee.com/p/..."
				class="flex-1 px-3 py-2 rounded-lg border border-amber-200 bg-white text-sm
					focus:outline-none focus:ring-2 focus:ring-amber-400/50" />
			<button type="button" onclick={handleScrape}
				disabled={scraping || !scrapeUrl.trim()}
				class="px-4 py-2 bg-amber-700 text-white rounded-lg text-sm hover:bg-amber-800
					transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
				{scraping ? 'Fetching...' : 'Fetch'}
			</button>
		</div>
		{#if scrapeError}<p class="text-sm text-red-500 mt-1">{scrapeError}</p>{/if}
		{#if scraped}
			<p class="text-sm text-green-600 mt-1">Filled from {scraped.roastery}</p>
			{#if scraped.flavor_descriptors?.uk?.length}
				<p class="text-xs text-amber-500 mt-0.5">UA: {scraped.flavor_descriptors.uk.join(', ')}</p>
			{/if}
		{/if}
	</div>

	<form onsubmit={handleSubmit} class="bg-white rounded-2xl border border-stone-100 shadow-sm p-6 space-y-4">
		{#if imageUrl}
			<div class="flex justify-center bg-stone-50 rounded-xl p-4">
				<img src={imageUrl} alt={name} class="h-32 object-contain" />
			</div>
		{/if}

		<div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
			<div>
				<label for="name" class="block text-xs text-stone-400 mb-1">Name *</label>
				<input id="name" type="text" bind:value={name} required
					class="w-full px-3 py-2 rounded-lg border border-stone-200 text-sm bg-white
						focus:outline-none focus:ring-2 focus:ring-amber-400/50" placeholder="Ethiopia Yirgacheffe" />
			</div>
			<div>
				<label for="roastery" class="block text-xs text-stone-400 mb-1">Roastery *</label>
				<input id="roastery" type="text" bind:value={roastery} required
					class="w-full px-3 py-2 rounded-lg border border-stone-200 text-sm bg-white
						focus:outline-none focus:ring-2 focus:ring-amber-400/50" placeholder="Local Roasters" />
			</div>
		</div>

		<div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
			<div>
				<label for="origin" class="block text-xs text-stone-400 mb-1">Origin</label>
				<input id="origin" type="text" bind:value={origin}
					class="w-full px-3 py-2 rounded-lg border border-stone-200 text-sm bg-white
						focus:outline-none focus:ring-2 focus:ring-amber-400/50" placeholder="Ethiopia" />
			</div>
			<div>
				<label for="process" class="block text-xs text-stone-400 mb-1">Process</label>
				<input id="process" type="text" bind:value={process}
					class="w-full px-3 py-2 rounded-lg border border-stone-200 text-sm bg-white
						focus:outline-none focus:ring-2 focus:ring-amber-400/50" placeholder="Washed" />
			</div>
			<div>
				<label for="roast_level" class="block text-xs text-stone-400 mb-1">Roast Level</label>
				<input id="roast_level" type="text" bind:value={roastLevel}
					class="w-full px-3 py-2 rounded-lg border border-stone-200 text-sm bg-white
						focus:outline-none focus:ring-2 focus:ring-amber-400/50" placeholder="Light" />
			</div>
		</div>

		{#if score || sweetness || acidity || bitterness}
			<div class="flex gap-6 p-3 bg-stone-50 rounded-xl">
				{#if score}<div class="text-center"><p class="text-lg font-bold text-amber-700">{score}</p><p class="text-[10px] text-stone-300 uppercase">Score</p></div>{/if}
				{#if sweetness}<div class="text-center"><p class="text-sm font-semibold">{sweetness}</p><p class="text-[10px] text-stone-300 uppercase">Sweet</p></div>{/if}
				{#if acidity}<div class="text-center"><p class="text-sm font-semibold">{acidity}</p><p class="text-[10px] text-stone-300 uppercase">Acid</p></div>{/if}
				{#if bitterness}<div class="text-center"><p class="text-sm font-semibold">{bitterness}</p><p class="text-[10px] text-stone-300 uppercase">Bitter</p></div>{/if}
			</div>
		{/if}

		<div>
			<label for="notes" class="block text-xs text-stone-400 mb-1">Notes</label>
			<textarea id="notes" bind:value={notes} rows={2}
				class="w-full px-3 py-2 rounded-lg border border-stone-200 text-sm bg-white
					focus:outline-none focus:ring-2 focus:ring-amber-400/50 resize-none"
				placeholder="Any notes..."></textarea>
		</div>

		<div>
			<p class="text-xs text-stone-400 mb-2">Roastery Descriptors</p>
			<DescriptorAutocomplete {descriptors} selected={selectedDescriptors} onToggle={toggleDescriptor} />
		</div>

		<div class="pt-2 flex gap-3">
			<button type="submit" disabled={saving || !name.trim() || !roastery.trim()}
				class="px-6 py-2.5 bg-amber-700 text-white rounded-lg hover:bg-amber-800
					transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed">
				{saving ? 'Saving...' : 'Add Coffee'}
			</button>
			<button type="button" onclick={onCancel}
				class="px-6 py-2.5 text-stone-400 hover:text-stone-600 transition-colors">Cancel</button>
		</div>
	</form>
</div>
