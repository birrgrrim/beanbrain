<script lang="ts">
	import type { CoffeeListItem } from '$lib/api';
	import { t } from '$lib/i18n';
	import { lang } from '$lib/lang';
	import Icons from './Icons.svelte';

	let currentLang = $state('en');
	lang.subscribe(v => currentLang = v);

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
				c.roastery_ref?.name.toLowerCase().includes(search.toLowerCase())
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

		{#if filteredCoffees.length === 0 && search}
			<div class="p-6 text-center">
				<p class="text-sm text-stone-500">{$t('sidebar.no_matches')}</p>
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
							<img src={coffee.image_url} alt="" class="w-16 h-16 rounded-lg object-contain flex-shrink-0 bg-card-inset" />
						{:else}
							<img src="/img/coffee-placeholder.png" alt="" class="w-16 h-16 flex-shrink-0 opacity-50" />
						{/if}
						<div class="flex items-center justify-between flex-1 min-w-0">
						<!-- Left: 3 lines -->
						<div class="min-w-0 flex-1">
							<p class="font-semibold text-lg text-stone-800 truncate">{coffee.name}</p>
							{#if coffee.origin_ref}
								<p class="text-sm text-stone-500 truncate">{coffee.origin_ref.flag ?? ''} {currentLang === 'uk' ? coffee.origin_ref.name_uk : coffee.origin_ref.name_en}</p>
							{/if}
							<p class="text-sm text-stone-400 truncate">{coffee.roastery_ref?.name}</p>
						</div>
						<!-- Right: rating + grind -->
						{#if coffee.person_rating != null || coffee.avg_rating != null || coffee.default_grind != null}
							{@const rating = coffee.person_rating ?? coffee.avg_rating}
							<div class="flex-shrink-0 ml-3 space-y-1">
								{#if rating != null}
									<div class="flex items-center justify-end" title="Rating">
										<img src="/img/icon-rating.png" alt="" class="w-8 h-8 {coffee.person_rating != null ? 'opacity-70' : 'opacity-30'}" />
										<span class="w-10 text-right text-2xl tabular-nums font-bold {coffee.person_rating != null ? 'text-amber-700' : 'text-stone-400'}">{Math.round(rating * 10) / 10}</span>
									</div>
								{/if}
								{#if coffee.default_grind != null}
									<div class="flex items-center justify-end" title="Grind setting">
										<img src="/img/icon-grind.png" alt="" class="w-8 h-8 opacity-50" />
										<span class="w-10 text-right text-2xl text-amber-700 tabular-nums font-bold">{coffee.default_grind}</span>
									</div>
								{/if}
							</div>
						{/if}
					</div>
					</div>
				</button>
			{/each}
		{/if}
	</div>
</aside>
