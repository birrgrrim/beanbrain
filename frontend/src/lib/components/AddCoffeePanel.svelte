<script lang="ts">
	import { api, type Descriptor, type ScrapeResult } from '$lib/api';
	import { t } from '$lib/i18n';
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
	let sweetness = $state<number | undefined>();
	let acidity = $state<number | undefined>();
	let bitterness = $state<number | undefined>();
	let notes = $state('');
	let roasterComment = $state<Record<string, string>>({});
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
			sweetness = result.sweetness ?? undefined;
			acidity = result.acidity ?? undefined;
			bitterness = result.bitterness ?? undefined;

			roasterComment = result.roaster_comment || {};

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
			sweetness,
			acidity,
			bitterness,
			notes: notes.trim() || undefined,
			roaster_comment: Object.keys(roasterComment).length > 0 ? JSON.stringify(roasterComment) : undefined,
			roastery_descriptor_ids: selectedDescriptors.length > 0 ? selectedDescriptors : undefined,
		});
		onCreated(coffee.id);
	}
</script>

<div class="max-w-2xl mx-auto p-6 space-y-6">
	<div class="flex items-center justify-between">
		<h2 class="text-2xl font-bold text-stone-800" style="font-family: 'DM Serif Display', serif;">
			{$t('add.title')}
		</h2>
		<button onclick={onCancel}
			class="px-4 py-2 text-sm text-stone-500 hover:text-stone-700 bg-card-inset hover:bg-parchment
				rounded-lg transition-colors font-medium">
			{$t('add.cancel')}
		</button>
	</div>

	<!-- URL Auto-fill -->
	<div class="bg-card rounded-2xl border border-amber-200 p-4">
		<div class="flex items-center gap-2 mb-2">
			<Icons icon="link" size={14} className="text-amber-500" />
			<p class="text-sm font-medium text-amber-700">{$t('add.url_hint')}</p>
		</div>
		<div class="flex gap-2">
			<input type="url" bind:value={scrapeUrl}
				placeholder="https://madheadscoffee.com/p/..."
				class="flex-1 px-3 py-2 rounded-lg border border-amber-200 bg-card text-sm
					focus:outline-none focus:ring-2 focus:ring-amber-400/50" />
			<button type="button" onclick={handleScrape}
				disabled={scraping || !scrapeUrl.trim()}
				class="px-4 py-2 bg-amber-700 text-white rounded-lg text-sm hover:bg-amber-800
					transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
				{scraping ? $t('add.fetching') : $t('add.fetch')}
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

	<form onsubmit={handleSubmit} class="bg-card rounded-2xl border border-stone-100 shadow-sm p-6 space-y-4">
		{#if imageUrl}
			<div class="flex justify-center bg-card-inset rounded-xl p-4">
				<img src={imageUrl} alt={name} class="h-32 object-contain" />
			</div>
		{/if}

		<div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
			<div>
				<label for="name" class="block text-xs text-stone-400 mb-1">{$t('add.name')} *</label>
				<input id="name" type="text" bind:value={name} required
					class="w-full px-3 py-2 rounded-lg border border-stone-200 text-sm bg-card
						focus:outline-none focus:ring-2 focus:ring-amber-400/50" placeholder="Ethiopia Yirgacheffe" />
			</div>
			<div>
				<label for="roastery" class="block text-xs text-stone-400 mb-1">{$t('add.roastery')} *</label>
				<input id="roastery" type="text" bind:value={roastery} required
					class="w-full px-3 py-2 rounded-lg border border-stone-200 text-sm bg-card
						focus:outline-none focus:ring-2 focus:ring-amber-400/50" placeholder="Local Roasters" />
			</div>
		</div>

		<div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
			<div>
				<label for="origin" class="block text-xs text-stone-400 mb-1">{$t('add.origin')}</label>
				<input id="origin" type="text" bind:value={origin}
					class="w-full px-3 py-2 rounded-lg border border-stone-200 text-sm bg-card
						focus:outline-none focus:ring-2 focus:ring-amber-400/50" placeholder="Ethiopia" />
			</div>
			<div>
				<label for="process" class="block text-xs text-stone-400 mb-1">{$t('add.process')}</label>
				<input id="process" type="text" bind:value={process}
					class="w-full px-3 py-2 rounded-lg border border-stone-200 text-sm bg-card
						focus:outline-none focus:ring-2 focus:ring-amber-400/50" placeholder="Washed" />
			</div>
			<div>
				<label for="roast_level" class="block text-xs text-stone-400 mb-1">{$t('add.roast_level')}</label>
				<input id="roast_level" type="text" bind:value={roastLevel}
					class="w-full px-3 py-2 rounded-lg border border-stone-200 text-sm bg-card
						focus:outline-none focus:ring-2 focus:ring-amber-400/50" placeholder="Light" />
			</div>
		</div>

		{#if score || sweetness != null || acidity != null || bitterness != null}
			<div class="flex gap-6 p-3 bg-card-inset rounded-xl">
				{#if score}<div class="text-center"><p class="text-lg font-bold text-amber-700">{score}</p><p class="text-[10px] text-stone-300 uppercase">{$t('detail.score')}</p></div>{/if}
				{#if sweetness != null}<div class="text-center"><p class="text-sm font-semibold">{sweetness}/10</p><p class="text-[10px] text-stone-300 uppercase">{$t('detail.sweet')}</p></div>{/if}
				{#if acidity != null}<div class="text-center"><p class="text-sm font-semibold">{acidity}/10</p><p class="text-[10px] text-stone-300 uppercase">{$t('detail.acid')}</p></div>{/if}
				{#if bitterness != null}<div class="text-center"><p class="text-sm font-semibold">{bitterness}/10</p><p class="text-[10px] text-stone-300 uppercase">{$t('detail.bitter')}</p></div>{/if}
			</div>
		{/if}

		<div>
			<label for="notes" class="block text-xs text-stone-400 mb-1">{$t('add.notes')}</label>
			<textarea id="notes" bind:value={notes} rows={2}
				class="w-full px-3 py-2 rounded-lg border border-stone-200 text-sm bg-card
					focus:outline-none focus:ring-2 focus:ring-amber-400/50 resize-none"
				placeholder="Any notes..."></textarea>
		</div>

		<div>
			<p class="text-xs text-stone-400 mb-2">{$t('add.descriptors')}</p>
			<DescriptorAutocomplete {descriptors} selected={selectedDescriptors} onToggle={toggleDescriptor} />
		</div>

		<div class="pt-2">
			<button type="submit" disabled={saving || !name.trim() || !roastery.trim()}
				class="px-6 py-2.5 bg-amber-700 text-white rounded-lg hover:bg-amber-800
					transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed">
				{saving ? $t('add.saving') : $t('add.save')}
			</button>
		</div>
	</form>
</div>
