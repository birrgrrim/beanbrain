<script lang="ts">
	import type { Descriptor } from '$lib/api';

	let { descriptors, selected = [], onToggle }: {
		descriptors: Descriptor[];
		selected: number[];
		onToggle: (id: number) => void;
	} = $props();

	let expandedCategory = $state<string | null>(null);

	const grouped = $derived(
		descriptors.reduce<Record<string, Descriptor[]>>((acc, d) => {
			(acc[d.category] ??= []).push(d);
			return acc;
		}, {})
	);
</script>

<div class="space-y-2">
	{#each Object.entries(grouped) as [category, items]}
		<div>
			<button
				type="button"
				class="text-sm font-medium text-stone-600 hover:text-stone-900 transition-colors"
				onclick={() => expandedCategory = expandedCategory === category ? null : category}
			>
				{category}
				<span class="text-xs text-stone-400">{expandedCategory === category ? '−' : '+'}</span>
			</button>

			{#if expandedCategory === category}
				<div class="flex flex-wrap gap-1.5 mt-1">
					{#each items as desc}
						{@const isSelected = selected.includes(desc.id)}
						<button
							type="button"
							class="px-2 py-0.5 rounded-full text-xs transition-colors
								{isSelected
									? 'bg-amber-600 text-white'
									: 'bg-stone-200 text-stone-600 hover:bg-stone-300'}"
							onclick={() => onToggle(desc.id)}
						>
							{desc.name}
						</button>
					{/each}
				</div>
			{/if}
		</div>
	{/each}

	{#if selected.length > 0}
		<div class="flex flex-wrap gap-1 pt-1 border-t border-stone-200">
			{#each selected as id}
				{@const desc = descriptors.find(d => d.id === id)}
				{#if desc}
					<span class="px-2 py-0.5 rounded-full text-xs bg-amber-100 text-amber-800">
						{desc.name}
						<button type="button" class="ml-1 hover:text-amber-600" onclick={() => onToggle(id)}>&times;</button>
					</span>
				{/if}
			{/each}
		</div>
	{/if}
</div>
