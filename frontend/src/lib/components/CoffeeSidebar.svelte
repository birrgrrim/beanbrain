<script lang="ts">
	import type { CoffeeListItem, Origin, Roastery, Descriptor } from '$lib/api';
	import { refData } from '$lib/refData';
	import { toggleId } from '$lib/utils';
	import { t } from '$lib/i18n';
	import { lang } from '$lib/lang';
	import SidebarShell from './SidebarShell.svelte';
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

	// Ref data for filter options
	let origins = $state<Origin[]>([]);
	let roasteries = $state<Roastery[]>([]);
	let descriptors = $state<Descriptor[]>([]);

	$effect(() => {
		Promise.all([refData.origins(), refData.roasteries(), refData.descriptors()]).then(([o, r, d]) => {
			origins = o;
			roasteries = r;
			descriptors = d;
		});
	});

	// --- Persisted state ---
	type SortKey = 'date' | 'rating' | 'price' | 'name';

	function loadState<T>(key: string, fallback: T): T {
		try {
			const v = localStorage.getItem(`bb_sidebar_${key}`);
			return v != null ? JSON.parse(v) : fallback;
		} catch { return fallback; }
	}
	function saveState(key: string, value: unknown) {
		localStorage.setItem(`bb_sidebar_${key}`, JSON.stringify(value));
	}

	let search = $state('');
	let showSort = $state(loadState('showSort', false));
	let showFilters = $state(loadState('showFilters', false));
	let hideUnavailable = $state(loadState('hideUnavailable', false));
	let filterOriginIds = $state<number[]>(loadState('filterOriginIds', []));
	let filterRoasteryIds = $state<number[]>(loadState('filterRoasteryIds', []));
	let filterRoastLevels = $state<string[]>(loadState('filterRoastLevels', []));
	let filterMinRating = $state<number>(loadState('filterMinRating', 0));
	let filterDescriptorIds = $state<number[]>(loadState('filterDescriptorIds', []));
	let sortKey = $state<SortKey>(loadState('sortKey', 'date'));
	let sortAsc = $state<boolean>(loadState('sortAsc', false));

	// Persist on change
	$effect(() => { saveState('showSort', showSort); });
	$effect(() => { saveState('showFilters', showFilters); });
	$effect(() => { saveState('hideUnavailable', hideUnavailable); });
	$effect(() => { saveState('filterOriginIds', filterOriginIds); });
	$effect(() => { saveState('filterRoasteryIds', filterRoasteryIds); });
	$effect(() => { saveState('filterRoastLevels', filterRoastLevels); });
	$effect(() => { saveState('filterMinRating', filterMinRating); });
	$effect(() => { saveState('filterDescriptorIds', filterDescriptorIds); });
	$effect(() => { saveState('sortKey', sortKey); });
	$effect(() => { saveState('sortAsc', sortAsc); });

	// Roast levels derived from actual data
	const availableRoastLevels = $derived(
		[...new Set(coffees.map(c => c.roast_level).filter((r): r is string => !!r))].sort()
	);

	const hasActiveFilters = $derived(
		hideUnavailable || filterOriginIds.length > 0 || filterRoasteryIds.length > 0 ||
		filterRoastLevels.length > 0 || filterMinRating > 0 || filterDescriptorIds.length > 0
	);

	const hasNonDefaultSort = $derived(sortKey !== 'date' || sortAsc);

	function clearFilters() {
		hideUnavailable = false;
		filterOriginIds = [];
		filterRoasteryIds = [];
		filterRoastLevels = [];
		filterMinRating = 0;
		filterDescriptorIds = [];
	}

	function toggleSort(key: SortKey) {
		if (sortKey === key) {
			sortAsc = !sortAsc;
		} else {
			sortKey = key;
			sortAsc = key === 'name'; // name defaults A-Z, others descending
		}
	}

	// --- Filter + sort pipeline ---
	const processedCoffees = $derived.by(() => {
		let list = coffees;

		// Text search
		if (search.trim()) {
			const q = search.toLowerCase();
			list = list.filter(c =>
				c.name.toLowerCase().includes(q) ||
				c.roastery_ref?.name.toLowerCase().includes(q)
			);
		}

		// Filters
		if (hideUnavailable) list = list.filter(c => c.is_available);
		if (filterOriginIds.length > 0) list = list.filter(c => c.origin_id != null && filterOriginIds.includes(c.origin_id));
		if (filterRoasteryIds.length > 0) list = list.filter(c => filterRoasteryIds.includes(c.roastery_id));
		if (filterRoastLevels.length > 0) list = list.filter(c => c.roast_level != null && filterRoastLevels.includes(c.roast_level));
		if (filterMinRating > 0) list = list.filter(c => {
			const r = c.person_rating ?? c.avg_rating;
			return r != null && r >= filterMinRating;
		});
		if (filterDescriptorIds.length > 0) list = list.filter(c =>
			filterDescriptorIds.some(did => c.roastery_descriptors.some(d => d.id === did))
		);

		// Sort
		const sorted = [...list];
		sorted.sort((a, b) => {
			let cmp = 0;
			if (sortKey === 'date') {
				cmp = new Date(a.created_at).getTime() - new Date(b.created_at).getTime();
			} else if (sortKey === 'rating') {
				const ra = a.person_rating ?? a.avg_rating ?? -1;
				const rb = b.person_rating ?? b.avg_rating ?? -1;
				cmp = ra - rb;
			} else if (sortKey === 'price') {
				const pa = a.price_wholesale ?? a.price ?? 99999;
				const pb = b.price_wholesale ?? b.price ?? 99999;
				cmp = pa - pb;
			} else if (sortKey === 'name') {
				cmp = a.name.localeCompare(b.name);
			}
			return sortAsc ? cmp : -cmp;
		});

		// Always keep unavailable at bottom regardless of sort (unless hidden)
		if (!hideUnavailable && sortKey !== 'date') {
			const available = sorted.filter(c => c.is_available);
			const unavailable = sorted.filter(c => !c.is_available);
			return [...available, ...unavailable];
		}

		return sorted;
	});

	// Descriptor search within filter
	let descriptorSearch = $state('');
	const filteredDescriptors = $derived(
		descriptorSearch.trim()
			? descriptors.filter(d => d.name.toLowerCase().includes(descriptorSearch.toLowerCase()))
			: descriptors.filter(d => filterDescriptorIds.includes(d.id))
	);
</script>

<aside class="w-[420px] flex-shrink-0 bg-card border-r border-stone-200 flex flex-col">
	<!-- Search + sort/filter toggles -->
	<div class="p-4 border-b border-stone-100 space-y-2">
		<div class="flex gap-2">
			<div class="relative flex-1">
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
			<button onclick={() => showSort = !showSort}
				class="p-1.5 rounded-lg border transition-colors flex-shrink-0
					{showSort || hasNonDefaultSort ? 'border-amber-300 bg-amber-50' : 'border-stone-200 bg-card-inset'}"
				title="Sort">
				<img src="/img/sort-beans.png" alt="" class="w-8 h-8 {showSort || hasNonDefaultSort ? 'opacity-80' : 'opacity-40'}" />
			</button>
			<button onclick={() => showFilters = !showFilters}
				class="p-1.5 rounded-lg border transition-colors flex-shrink-0
					{showFilters || hasActiveFilters ? 'border-amber-300 bg-amber-50' : 'border-stone-200 bg-card-inset'}"
				title={$t('sidebar.filters')}>
				<img src="/img/filter-icon.png" alt="" class="w-8 h-8 {showFilters || hasActiveFilters ? 'opacity-80' : 'opacity-40'}" />
			</button>
		</div>

		<!-- Sort panel -->
		{#if showSort}
			<div class="flex gap-1">
				{#each [
					{ key: 'date', label: $t('sidebar.sort_date') },
					{ key: 'rating', label: $t('sidebar.sort_rating') },
					{ key: 'price', label: $t('sidebar.sort_price') },
					{ key: 'name', label: $t('sidebar.sort_name') },
				] as opt}
					<button
						onclick={() => toggleSort(opt.key as SortKey)}
						class="px-2.5 py-1 rounded text-xs font-medium transition-colors
							{sortKey === opt.key
								? 'bg-amber-100 text-amber-800'
								: 'text-stone-400 hover:text-stone-600 hover:bg-card-inset'}"
					>
						{opt.label}
						{#if sortKey === opt.key}
							<span class="ml-0.5">{sortAsc ? '↑' : '↓'}</span>
						{/if}
					</button>
				{/each}
			</div>
		{/if}

		<!-- Filters panel -->
		{#if showFilters}
			<div class="space-y-2.5 pt-1">
				<!-- Availability toggle -->
				<label class="flex items-center gap-2 cursor-pointer">
					<input type="checkbox" bind:checked={hideUnavailable}
						class="rounded border-stone-300 text-amber-600 focus:ring-amber-400/50" />
					<span class="text-xs text-stone-500">{$t('sidebar.hide_unavailable')}</span>
				</label>

				<!-- Origin -->
				{#if origins.length > 0}
					<div>
						<p class="text-[10px] text-stone-400 uppercase tracking-wide mb-1">{$t('sidebar.origin')}</p>
						<div class="flex flex-wrap gap-1">
							{#each origins.filter(o => coffees.some(c => c.origin_id === o.id)) as origin}
								{@const active = filterOriginIds.includes(origin.id)}
								<button
									onclick={() => filterOriginIds = toggleId(filterOriginIds, origin.id)}
									class="px-2 py-0.5 rounded-full text-xs border transition-colors
										{active ? 'bg-amber-100 border-amber-300 text-amber-800' : 'border-stone-200 text-stone-400 hover:border-stone-300'}"
								>
									{origin.flag ?? ''} {currentLang === 'uk' ? origin.name_uk : origin.name_en}
								</button>
							{/each}
						</div>
					</div>
				{/if}

				<!-- Roastery -->
				{#if roasteries.length > 1}
					<div>
						<p class="text-[10px] text-stone-400 uppercase tracking-wide mb-1">{$t('sidebar.roastery')}</p>
						<div class="flex flex-wrap gap-1">
							{#each roasteries.filter(r => coffees.some(c => c.roastery_id === r.id)) as roastery}
								{@const active = filterRoasteryIds.includes(roastery.id)}
								<button
									onclick={() => filterRoasteryIds = toggleId(filterRoasteryIds, roastery.id)}
									class="px-2 py-0.5 rounded-full text-xs border transition-colors
										{active ? 'bg-amber-100 border-amber-300 text-amber-800' : 'border-stone-200 text-stone-400 hover:border-stone-300'}"
								>
									{roastery.name}
								</button>
							{/each}
						</div>
					</div>
				{/if}

				<!-- Roast level -->
				{#if availableRoastLevels.length > 0}
					<div>
						<p class="text-[10px] text-stone-400 uppercase tracking-wide mb-1">{$t('sidebar.roast')}</p>
						<div class="flex flex-wrap gap-1">
							{#each availableRoastLevels as level}
								{@const active = filterRoastLevels.includes(level)}
								<button
									onclick={() => filterRoastLevels = active ? filterRoastLevels.filter(l => l !== level) : [...filterRoastLevels, level]}
									class="px-2 py-0.5 rounded-full text-xs border transition-colors
										{active ? 'bg-amber-100 border-amber-300 text-amber-800' : 'border-stone-200 text-stone-400 hover:border-stone-300'}"
								>
									{level}
								</button>
							{/each}
						</div>
					</div>
				{/if}

				<!-- Rating min -->
				<div>
					<p class="text-[10px] text-stone-400 uppercase tracking-wide mb-1">{$t('sidebar.rating_min')} {filterMinRating > 0 ? `≥ ${filterMinRating}` : ''}</p>
					<input type="range" min="0" max="10" step="1" bind:value={filterMinRating}
						class="w-full h-1.5 rounded-full appearance-none bg-stone-200 accent-amber-600" />
				</div>

				<!-- Descriptors -->
				<div>
					<p class="text-[10px] text-stone-400 uppercase tracking-wide mb-1">{$t('sidebar.descriptors')}</p>
					<input type="text" bind:value={descriptorSearch} placeholder="..."
						class="w-full px-2 py-1 rounded border border-stone-200 text-xs bg-card-inset
							focus:outline-none focus:ring-1 focus:ring-amber-400/50 placeholder:text-stone-300" />
					{#if filteredDescriptors.length > 0}
						<div class="flex flex-wrap gap-1 mt-1 max-h-20 overflow-y-auto">
							{#each filteredDescriptors as desc}
								{@const active = filterDescriptorIds.includes(desc.id)}
								<button
									onclick={() => { filterDescriptorIds = toggleId(filterDescriptorIds, desc.id); descriptorSearch = ''; }}
									class="px-2 py-0.5 rounded-full text-xs border transition-colors
										{active ? 'bg-amber-100 border-amber-300 text-amber-800' : 'border-stone-200 text-stone-400 hover:border-stone-300'}"
								>
									{desc.name}
								</button>
							{/each}
						</div>
					{/if}
				</div>

				<!-- Clear all -->
				{#if hasActiveFilters}
					<button onclick={clearFilters}
						class="text-xs text-amber-600 hover:text-amber-800 font-medium">
						{$t('sidebar.clear_filters')}
					</button>
				{/if}
			</div>
		{/if}
	</div>

	<!-- Coffee list -->
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

		{#if processedCoffees.length === 0 && (search || hasActiveFilters)}
			<div class="p-6 text-center">
				<p class="text-sm text-stone-500">{$t('sidebar.no_matches')}</p>
			</div>
		{:else}
			{#each processedCoffees as coffee}
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
							<p class="text-sm text-stone-400 truncate">{coffee.roastery_ref?.name}{#if coffee.price != null} · {coffee.price_wholesale != null ? coffee.price_wholesale : coffee.price}₴{/if}</p>
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
