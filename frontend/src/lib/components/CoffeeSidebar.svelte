<script lang="ts">
	import type { CoffeeListItem } from '$lib/api';
	import { t } from '$lib/i18n';
	import Icons from './Icons.svelte';

	let { coffees = [], selectedId = null, onSelect, onAdd, onRefresh }: {
		coffees: CoffeeListItem[];
		selectedId: number | null;
		onSelect: (id: number) => void;
		onAdd: () => void;
		onRefresh: () => void;
	} = $props();

	let search = $state('');
	let filteredCoffees = $derived(
		search.trim()
			? coffees.filter(c =>
				c.name.toLowerCase().includes(search.toLowerCase()) ||
				c.roastery.toLowerCase().includes(search.toLowerCase())
			)
			: coffees
	);
</script>

<aside class="w-80 flex-shrink-0 bg-white border-r border-stone-200 flex flex-col">
	<!-- Header -->
	<div class="p-4 border-b border-stone-100">
		<div class="flex items-center justify-between mb-3">
			<span class="text-sm font-semibold text-stone-600">{$t('tab.coffee')}</span>
			<button
				onclick={onAdd}
				class="w-8 h-8 flex items-center justify-center rounded-lg
					bg-amber-700 text-white hover:bg-amber-800 transition-colors"
				title="Add coffee"
			>
				<Icons icon="plus" size={16} />
			</button>
		</div>

		<div class="relative">
			<Icons icon="search" size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-stone-300" />
			<input
				type="text"
				bind:value={search}
				placeholder={$t('sidebar.search')}
				class="w-full pl-8 pr-3 py-2 rounded-lg border border-stone-200 bg-stone-50 text-sm
					focus:outline-none focus:ring-2 focus:ring-amber-400/50 focus:border-amber-300
					placeholder:text-stone-300"
			/>
		</div>
	</div>

	<div class="flex-1 overflow-y-auto">
		{#if filteredCoffees.length === 0}
			<div class="p-8 text-center">
				<Icons icon="bean" size={32} className="mx-auto text-stone-200 mb-2" />
				<p class="text-sm text-stone-400">
					{search ? $t('sidebar.no_matches') : $t('sidebar.empty')}
				</p>
			</div>
		{:else}
			{#each filteredCoffees as coffee}
				<button
					onclick={() => onSelect(coffee.id)}
					class="w-full text-left px-4 py-2.5 border-b border-stone-50 transition-colors
						hover:bg-amber-50/50
						{selectedId === coffee.id ? 'bg-amber-50 border-l-2 border-l-amber-600' : ''}
						{!coffee.is_available ? 'opacity-40' : ''}"
				>
					<div class="flex items-center gap-3">
						{#if coffee.image_url}
							<img src={coffee.image_url} alt="" class="w-10 h-10 rounded-lg object-contain flex-shrink-0 bg-stone-50" />
						{:else}
							<div class="w-10 h-10 rounded-lg bg-stone-100 flex items-center justify-center flex-shrink-0">
								<Icons icon="bean" size={18} className="text-stone-300" />
							</div>
						{/if}
						<div class="min-w-0 flex-1">
							<p class="font-medium text-sm text-stone-800 truncate">{coffee.name}</p>
							<div class="flex items-center gap-2 mt-0.5">
								<span class="text-xs text-stone-400 truncate">{coffee.roastery}</span>
								{#if coffee.default_grind != null || coffee.avg_rating != null}
									<span class="text-stone-200">|</span>
									{#if coffee.default_grind != null}
										<span class="text-xs text-stone-400 tabular-nums">{coffee.default_grind}</span>
									{/if}
									{#if coffee.avg_rating != null}
										<span class="text-xs text-amber-500 tabular-nums">{(coffee.avg_rating / 2).toFixed(1)}<span class="text-amber-400">&#9733;</span></span>
									{/if}
								{/if}
							</div>
						</div>
					</div>
				</button>
			{/each}
		{/if}
	</div>
</aside>
