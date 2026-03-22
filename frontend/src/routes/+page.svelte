<script lang="ts">
	import { api, type CoffeeListItem } from '$lib/api';
	import { lang, type Lang } from '$lib/lang';
	import { activePerson } from '$lib/personStore';
	import { activeGrinder, activeBrewSetup } from '$lib/contextStore';
	import { appMode, type AppMode } from '$lib/modeStore';
	import { t } from '$lib/i18n';
	import ContextSwitcher from '$lib/components/ContextSwitcher.svelte';
	import CoffeeDetail from '$lib/components/CoffeeDetail.svelte';
	import AddCoffeePanel from '$lib/components/AddCoffeePanel.svelte';
	import CoffeeCard from '$lib/components/CoffeeCard.svelte';
	import EmptyState from '$lib/components/EmptyState.svelte';

	type View = { type: 'grid' } | { type: 'detail'; id: number } | { type: 'new' };

	let allCoffees = $state<CoffeeListItem[]>([]);
	let view = $state<View>({ type: 'grid' });
	let searchQuery = $state('');

	let currentLang = $state<Lang>('en');
	let currentMode = $state<AppMode>('my-coffee');
	let currentPersonId = $state<number | null>(null);
	let currentGrinderId = $state<number | null>(null);
	let currentBrewSetupId = $state<number | null>(null);

	lang.subscribe(v => currentLang = v);
	appMode.subscribe(v => currentMode = v);
	activePerson.subscribe(v => currentPersonId = v);
	activeGrinder.subscribe(v => currentGrinderId = v);
	activeBrewSetup.subscribe(v => currentBrewSetupId = v);

	async function loadCoffees() {
		allCoffees = await api.coffees.list({
			tasterId: currentPersonId,
			grinderId: currentGrinderId,
			brewSetupId: currentBrewSetupId,
		});
	}

	$effect(() => { currentPersonId; currentGrinderId; currentBrewSetupId; loadCoffees(); });

	const filteredCoffees = $derived.by(() => {
		let list = allCoffees;

		if (currentMode === 'my-coffee') {
			list = list.filter(c => c.in_stock);
			list = [...list].sort((a, b) => a.name.localeCompare(b.name));
		} else {
			if (searchQuery.trim()) {
				const q = searchQuery.toLowerCase();
				list = list.filter(c =>
					c.name.toLowerCase().includes(q) ||
					c.roastery_ref.name.toLowerCase().includes(q) ||
					(c.origin_ref?.name_en.toLowerCase().includes(q)) ||
					(c.origin_ref?.name_uk.toLowerCase().includes(q)) ||
					c.roastery_descriptors.some(d => d.name.toLowerCase().includes(q))
				);
			}
			list = [...list].sort((a, b) => b.created_at.localeCompare(a.created_at));
		}

		return list;
	});

	function selectCoffee(id: number) {
		view = { type: 'detail', id };
	}

	async function onCoffeeCreated(id: number) {
		await loadCoffees();
		view = { type: 'detail', id };
	}

	async function onCoffeeDeleted() {
		await loadCoffees();
		view = { type: 'grid' };
	}

	function backToGrid() {
		view = { type: 'grid' };
	}

	function toggleLang() {
		lang.set(currentLang === 'en' ? 'uk' : 'en');
	}

	function setMode(mode: AppMode) {
		appMode.set(mode);
		view = { type: 'grid' };
	}

	const appVersion = __APP_VERSION__;

	let innerWidth = $state(0);
	const isMobile = $derived(innerWidth < 768);
</script>

<svelte:window bind:innerWidth />

<div class="app-shell">
	<!-- Top bar -->
	<header class="topbar">
		<div class="topbar-inner">
			<img src="/img/logo-text.png" alt="BeanBrain" class="topbar-logo" />
			<div class="flex items-center gap-2">
				{#if currentMode === 'my-coffee'}
					<ContextSwitcher onChange={loadCoffees} />
				{:else}
					<div class="discover-context">
						<ContextSwitcher onChange={loadCoffees} />
					</div>
				{/if}
			</div>
		</div>
	</header>

	{#if view.type === 'grid'}
		<main class="flex-1 overflow-y-auto bg-parchment px-2 md:px-3 py-2 md:py-3"
			style="background-image: url('/img/bg-pattern.png'); background-repeat: repeat;">

			<!-- Controls row -->
			<div class="controls-row">
				<div class="controls-left">
					<button
						onclick={() => view = { type: 'new' }}
						class="add-btn"
						title={$t('add.title')}
					>
						<svg viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
							<path d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" />
						</svg>
						<span class="hidden md:inline">{$t('add.title')}</span>
					</button>
				</div>

				<div class="mode-toggle">
					<button
						class="mode-btn {currentMode === 'my-coffee' ? 'active' : ''}"
						onclick={() => setMode('my-coffee')}
					>
						{$t('mode.my_coffee')}
					</button>
					<button
						class="mode-btn {currentMode === 'discover' ? 'active' : ''}"
						onclick={() => setMode('discover')}
					>
						{$t('mode.discover')}
					</button>
				</div>

				<div class="controls-right hidden md:block">
					{#if currentMode === 'discover'}
						<div class="relative flex items-center">
							<svg class="absolute left-2.5 w-4 h-4 text-stone-400 pointer-events-none" viewBox="0 0 20 20" fill="currentColor">
								<path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
							</svg>
							<input
								type="text"
								bind:value={searchQuery}
								placeholder={$t('sidebar.search')}
								class="pl-8 pr-3 py-2 border border-stone-200 rounded-lg text-sm bg-card-inset
									focus:outline-none focus:border-amber-400 focus:ring-1 focus:ring-amber-200
									w-[240px] lg:w-[300px]"
							/>
						</div>
					{/if}
				</div>
			</div>

			<!-- Mobile search row (Discover only) -->
			{#if currentMode === 'discover'}
				<div class="md:hidden mb-2">
					<div class="relative flex items-center">
						<svg class="absolute left-2.5 w-4 h-4 text-stone-400 pointer-events-none" viewBox="0 0 20 20" fill="currentColor">
							<path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
						</svg>
						<input
							type="text"
							bind:value={searchQuery}
							placeholder={$t('sidebar.search')}
							class="w-full pl-8 pr-3 py-2 border border-stone-200 rounded-lg text-sm bg-card-inset
								focus:outline-none focus:border-amber-400 focus:ring-1 focus:ring-amber-200"
						/>
					</div>
				</div>
			{/if}

			<!-- Cards grid -->
			{#if filteredCoffees.length === 0}
				<div class="flex items-center justify-center" style="min-height: 60vh;">
					<EmptyState
						img={currentMode === 'my-coffee' ? 'empty-shelf.png' : 'choose-coffee.png'}
						title={$t(currentMode === 'my-coffee' ? 'empty.my_coffee' : 'empty.discover')}
						subtitle={$t(currentMode === 'my-coffee' ? 'empty.my_coffee_hint' : 'empty.discover_hint')}
					/>
				</div>
			{:else}
				<div class="card-grid">
					{#each filteredCoffees as coffee, i (coffee.id)}
						<div class="animate-card-grid" style="animation-delay: {Math.min(i * 30, 300)}ms">
							<CoffeeCard {coffee} mode={currentMode} onClick={selectCoffee} />
						</div>
					{/each}
				</div>
			{/if}
		</main>

	{:else if view.type === 'detail'}
		<main class="flex-1 overflow-y-auto bg-parchment" style="background-image: url('/img/bg-pattern.png'); background-repeat: repeat;">
			<CoffeeDetail
				coffeeId={view.id}
				onDeleted={onCoffeeDeleted}
				onUpdated={loadCoffees}
				onBack={backToGrid}
			/>
		</main>

	{:else if view.type === 'new'}
		<main class="flex-1 overflow-y-auto bg-parchment" style="background-image: url('/img/bg-pattern.png'); background-repeat: repeat;">
			<AddCoffeePanel
				onCreated={onCoffeeCreated}
				onCancel={backToGrid}
			/>
		</main>
	{/if}

	<!-- Status bar -->
	<div class="statusbar">
		<div class="flex items-center gap-3">
			<a href="https://github.com/birrgrrim/beanbrain" target="_blank" rel="noopener" title="GitHub">
				<svg viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4">
					<path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
				</svg>
			</a>
		</div>
		<div class="flex items-center gap-4">
			<button
				onclick={toggleLang}
				class="flex items-center gap-1.5 hover:text-amber-700"
				style="color: inherit;"
			>
				{#if currentLang === 'en'}
					<span>🇬🇧</span> EN
				{:else}
					<span>🇺🇦</span> UA
				{/if}
			</button>
			<span class="text-stone-300">·</span>
			<button class="hover:text-amber-700" style="color: inherit;">
				{$t('footer.about')}
			</button>
		</div>
	</div>
</div>

<style>
	/* Top bar — proportional */
	.topbar {
		background: var(--color-card);
		border-bottom: 1px solid rgba(0, 0, 0, 0.08);
		flex-shrink: 0;
		position: relative;
		z-index: 20;
	}

	.app-shell {
		display: flex;
		flex-direction: column;
		height: 100vh;
		height: 100dvh;
		overflow: hidden;
		font-size: 1rem;
	}

	.topbar-inner {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 0.1rem 0.75rem;
	}

	@media (min-width: 768px) {
		.topbar-inner {
			padding: 0.1rem 1rem;
		}
	}

	.topbar-logo {
		object-fit: contain;
		height: 42px;
	}

	@media (min-width: 768px) {
		.topbar-logo {
			height: 48px;
		}
	}

	/* Controls row */
	.controls-row {
		display: grid;
		grid-template-columns: 1fr auto 1fr;
		align-items: center;
		gap: 0.75rem;
		margin-bottom: 0.75rem;
	}

	.controls-left {
		justify-self: start;
	}

	.controls-right {
		justify-self: end;
	}

	@media (min-width: 768px) {
		.controls-row {
			margin-bottom: 1rem;
		}
	}

	.add-btn {
		display: flex;
		align-items: center;
		gap: 0.3rem;
		padding: 0.4rem 0.75rem;
		border-radius: 0.5rem;
		font-size: 0.85rem;
		font-weight: 600;
		background: var(--color-amber-600, #d97706);
		color: white;
		border: none;
		cursor: pointer;
	}

	@media (min-width: 768px) {
		.add-btn {
			padding: 0.5rem 1rem;
			font-size: 0.9rem;
		}
	}

	.add-btn:hover {
		background: var(--color-amber-700, #b45309);
	}

	/* Card grid — auto-fill, 3 columns on ~1900px+ */
	.card-grid {
		display: grid;
		grid-template-columns: 1fr;
		gap: 0.5rem;
	}

	@media (min-width: 640px) {
		.card-grid {
			grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
			gap: 0.6rem;
		}
	}

	@media (min-width: 1024px) {
		.card-grid {
			grid-template-columns: repeat(auto-fill, minmax(480px, 1fr));
			gap: 0.6rem;
		}
	}

	@media (min-width: 1600px) {
		.card-grid {
			grid-template-columns: repeat(auto-fill, minmax(700px, 1fr));
			gap: 0.75rem;
		}
	}

	/* Status bar — proportional */
	.statusbar {
		background: var(--color-card);
		border-top: 1px solid rgba(0, 0, 0, 0.08);
		padding: 0.4rem 1rem;
		display: flex;
		align-items: center;
		justify-content: space-between;
		font-size: 0.75rem;
		color: #8c7b6b;
		flex-shrink: 0;
	}

	@media (min-width: 768px) {
		.statusbar {
			padding: 0.5rem 1.5rem;
			font-size: 0.8rem;
		}
	}

	.statusbar a {
		color: #8c7b6b;
		text-decoration: none;
	}

	.statusbar a:hover {
		color: var(--color-amber-700, #b45309);
	}

	/* Hide only grinder in discover mode (keep person + brew for rating) */
	.discover-context :global(.context-switcher > div:nth-child(2)) {
		display: none;
	}
</style>
