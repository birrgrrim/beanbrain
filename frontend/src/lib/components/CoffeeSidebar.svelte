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
	<div class="p-4 border-b border-stone-100">
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
		<!-- Add coffee card -->
		<button
			onclick={onAdd}
			class="w-full text-left px-5 py-3 border-b border-stone-50 transition-colors
				hover:bg-amber-50/50 group"
		>
			<div class="flex items-center gap-3">
				<img src="/img/add-coffee.png" alt="" class="w-20 h-20 opacity-50 group-hover:opacity-70 transition-opacity" />
				<p class="text-base font-medium text-amber-600 group-hover:text-amber-700">{$t('add.title')}</p>
			</div>
		</button>

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
							<img src={coffee.image_url} alt="" class="w-20 h-20 rounded-lg object-contain flex-shrink-0 bg-card-inset" />
						{:else}
							<img src="/img/coffee-placeholder.png" alt="" class="w-20 h-20 flex-shrink-0 opacity-50" />
						{/if}
						<div class="min-w-0 flex-1">
							<p class="font-semibold text-lg text-stone-800 truncate">{coffee.name}</p>
							<div class="flex items-center justify-between mt-0.5">
								<div class="min-w-0">
									<p class="text-sm text-stone-400 truncate">{coffee.roastery}</p>
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
								{#if coffee.default_grind != null}
									<div class="flex items-center gap-1 flex-shrink-0 ml-2" title="Grind setting">
										<img src="/img/burr-icon.png" alt="" class="w-6 h-6 opacity-40" />
										<span class="text-2xl text-amber-700 tabular-nums font-bold">{coffee.default_grind}</span>
									</div>
								{/if}
							</div>
						</div>
					</div>
				</button>
			{/each}
		{/if}
	</div>
</aside>
