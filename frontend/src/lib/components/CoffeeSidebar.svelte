<script lang="ts">
	import type { CoffeeListItem } from '$lib/api';
	import { t } from '$lib/i18n';
	import Icons from './Icons.svelte';
	import StarRating from './StarRating.svelte';

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

<aside class="w-[420px] flex-shrink-0 bg-card border-r border-stone-200 flex flex-col">
	<!-- Header -->
	<div class="p-4 border-b border-stone-100">
		<div class="flex items-center justify-between mb-3">
			<div class="flex items-center gap-2">
				<img src="/img/header-coffee.png" alt="" class="w-6 h-6 opacity-70" />
				<span class="text-sm font-semibold text-stone-600">{$t('tab.coffee')}</span>
			</div>
			<button
				onclick={onAdd}
				class="w-10 h-10 flex items-center justify-center rounded-lg
					bg-amber-700 text-white hover:bg-amber-800 transition-colors"
				title="Add coffee"
			>
				<Icons icon="plus" size={20} />
			</button>
		</div>

		<div class="relative">
			<Icons icon="search" size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-stone-300" />
			<input
				type="text"
				bind:value={search}
				placeholder={$t('sidebar.search')}
				class="w-full pl-9 pr-4 py-2.5 rounded-lg border border-stone-200 bg-card-inset text-base
					focus:outline-none focus:ring-2 focus:ring-amber-400/50 focus:border-amber-300
					placeholder:text-stone-400"
			/>
		</div>
	</div>

	<div class="flex-1 overflow-y-auto">
		{#if filteredCoffees.length === 0}
			<div class="p-6 text-center">
				<img src="/img/empty-shelf.png" alt="" class="mx-auto mb-3 opacity-80" style="max-width: 180px;" />
				<p class="text-sm text-stone-500">
					{search ? $t('sidebar.no_matches') : $t('sidebar.empty')}
				</p>
			</div>
		{:else}
			{#each filteredCoffees as coffee}
				<button
					onclick={() => onSelect(coffee.id)}
					class="w-full text-left px-5 py-4 border-b border-stone-50 transition-colors
						hover:bg-amber-50/50
						{selectedId === coffee.id ? 'bg-amber-50 border-l-2 border-l-amber-600' : ''}
						{!coffee.is_available ? 'opacity-40' : ''}"
				>
					<div class="flex items-center gap-3">
						{#if coffee.image_url}
							<img src={coffee.image_url} alt="" class="w-14 h-14 rounded-lg object-contain flex-shrink-0 bg-card-inset" />
						{:else}
							<div class="w-14 h-14 rounded-lg bg-card-inset flex items-center justify-center flex-shrink-0 overflow-hidden">
								<img src="/img/coffee-placeholder.png" alt="" class="w-10 h-10 opacity-60" />
							</div>
						{/if}
						<div class="min-w-0 flex-1">
							<p class="font-semibold text-lg text-stone-800 truncate">{coffee.name}</p>
							<div class="flex items-center gap-2 mt-0.5">
								<span class="text-sm text-stone-400 truncate">{coffee.roastery}</span>
								{#if coffee.default_grind != null}
									<span class="text-stone-200">|</span>
									<span class="text-base text-stone-500 tabular-nums font-medium" title="Grind setting">
										<img src="/img/burr-icon.png" alt="" class="w-6 h-6 inline opacity-50 mr-0.5" />{coffee.default_grind}
									</span>
								{/if}
							</div>
							{#if coffee.person_rating != null}
								<div class="mt-0.5">
									<StarRating rating={coffee.person_rating} size="sm" />
								</div>
							{:else if coffee.avg_rating != null}
								<div class="mt-0.5 opacity-50">
									<StarRating rating={Math.round(coffee.avg_rating)} size="sm" />
								</div>
							{/if}
						</div>
					</div>
				</button>
			{/each}
		{/if}
	</div>
</aside>
