<script lang="ts">
	import type { Descriptor } from '$lib/api';
	import { t } from '$lib/i18n';

	let { descriptors, selected = [], suggested = [], onToggle }: {
		descriptors: Descriptor[];
		selected: number[];
		suggested?: number[];
		onToggle: (id: number) => void;
	} = $props();

	let query = $state('');
	let focused = $state(false);

	const filtered = $derived(
		query.trim()
			? descriptors.filter(d =>
				d.name.toLowerCase().includes(query.toLowerCase()) &&
				!selected.includes(d.id)
			).slice(0, 8)
			: []
	);

	const unselectedSuggested = $derived(
		suggested.filter(id => !selected.includes(id))
	);

	function select(id: number) {
		onToggle(id);
		query = '';
	}
</script>

<div class="space-y-2">
	<!-- Suggested from roastery -->
	{#if unselectedSuggested.length > 0}
		<div>
			<p class="text-xs text-amber-600/80 mb-1">{$t('desc.suggested')}</p>
			<div class="flex flex-wrap gap-1.5">
				{#each unselectedSuggested as id}
					{@const desc = descriptors.find(d => d.id === id)}
					{#if desc}
						<button
							type="button"
							class="px-2.5 py-1 rounded-full text-xs bg-amber-50 text-amber-700
								border border-amber-200 hover:bg-amber-100 transition-colors"
							onclick={() => select(id)}
						>+ {desc.name}</button>
					{/if}
				{/each}
			</div>
		</div>
	{/if}

	<!-- Search input -->
	<div class="relative">
		<input
			type="text"
			bind:value={query}
			onfocus={() => focused = true}
			onblur={() => setTimeout(() => focused = false, 200)}
			placeholder={$t('desc.search')}
			class="w-full px-3 py-2 rounded-lg border border-stone-200 text-sm bg-white
				focus:outline-none focus:ring-2 focus:ring-amber-400/50 focus:border-amber-300
				placeholder:text-stone-300"
		/>

		{#if focused && filtered.length > 0}
			<div class="absolute z-10 mt-1 w-full bg-white rounded-lg border border-stone-200 shadow-lg overflow-hidden">
				{#each filtered as desc}
					<button
						type="button"
						class="w-full text-left px-3 py-2 text-sm hover:bg-amber-50 transition-colors
							flex items-center justify-between"
						onmousedown={() => select(desc.id)}
					>
						<span>{desc.name}</span>
						<span class="text-xs text-stone-300">{desc.category}</span>
					</button>
				{/each}
			</div>
		{/if}
	</div>

	<!-- Selected tags -->
	{#if selected.length > 0}
		<div class="flex flex-wrap gap-1.5">
			{#each selected as id}
				{@const desc = descriptors.find(d => d.id === id)}
				{#if desc}
					<span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs
						bg-amber-100 text-amber-800">
						{desc.name}
						<button type="button" class="hover:text-amber-600" title="Remove" onclick={() => onToggle(id)}>
							<svg class="w-3 h-3" viewBox="0 0 12 12"><path d="M3 3l6 6M9 3l-6 6" stroke="currentColor" stroke-width="1.5" fill="none"/></svg>
						</button>
					</span>
				{/if}
			{/each}
		</div>
	{/if}
</div>
