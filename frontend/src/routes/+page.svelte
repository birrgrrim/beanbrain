<script lang="ts">
	import { api, type CoffeeListItem, type Grinder, type BrewSetup, type Roastery } from '$lib/api';
	import { lang, type Lang } from '$lib/lang';
	import { activePerson } from '$lib/personStore';
	import { t } from '$lib/i18n';
	import CoffeeSidebar from '$lib/components/CoffeeSidebar.svelte';
	import CoffeeDetail from '$lib/components/CoffeeDetail.svelte';
	import AddCoffeePanel from '$lib/components/AddCoffeePanel.svelte';
	import GrindingSidebar from '$lib/components/GrindingSidebar.svelte';
	import GrinderDetail from '$lib/components/GrinderDetail.svelte';
	import AddGrinderPanel from '$lib/components/AddGrinderPanel.svelte';
	import BrewingSidebar from '$lib/components/BrewingSidebar.svelte';
	import BrewSetupDetail from '$lib/components/BrewSetupDetail.svelte';
	import BrewMethodPicker from '$lib/components/BrewMethodPicker.svelte';
	import AddBrewSetupPanel from '$lib/components/AddBrewSetupPanel.svelte';
	import RoasterySidebar from '$lib/components/RoasterySidebar.svelte';
	import RoasteryDetail from '$lib/components/RoasteryDetail.svelte';
	import AddRoasteryPanel from '$lib/components/AddRoasteryPanel.svelte';
	import PersonSwitcher from '$lib/components/PersonSwitcher.svelte';
	import EmptyState from '$lib/components/EmptyState.svelte';

	type Tab = 'coffee' | 'grinding' | 'brewing' | 'roasteries';
	type CoffeePanel = { type: 'empty' } | { type: 'detail'; id: number } | { type: 'new' };
	type GrinderPanel = { type: 'empty' } | { type: 'detail'; id: number } | { type: 'new' };
	type BrewPanel = { type: 'empty' } | { type: 'detail'; id: number } | { type: 'pick_method' } | { type: 'new'; methodType: string; hasBasket: boolean };
	type RoasteryPanel = { type: 'empty' } | { type: 'detail'; id: number } | { type: 'new' };

	let activeTab = $state<Tab>('coffee');
	let coffees = $state<CoffeeListItem[]>([]);
	let coffeePanel = $state<CoffeePanel>({ type: 'empty' });

	let grinders = $state<Grinder[]>([]);
	let grinderPanel = $state<GrinderPanel>({ type: 'empty' });

	let brewSetups = $state<BrewSetup[]>([]);
	let brewPanel = $state<BrewPanel>({ type: 'empty' });

	let roasteriesList = $state<Roastery[]>([]);
	let roasteryPanel = $state<RoasteryPanel>({ type: 'empty' });

	let currentLang = $state<Lang>('en');
	let currentPersonId = $state<number | null>(null);

	lang.subscribe(v => currentLang = v);
	activePerson.subscribe(v => currentPersonId = v);

	const tabDefs: { id: Tab; key: string; img: string }[] = [
		{ id: 'coffee', key: 'tab.coffee', img: '/img/tab-coffee.png' },
		{ id: 'grinding', key: 'tab.grinding', img: '/img/tab-grinder.png' },
		{ id: 'brewing', key: 'tab.brewing', img: '/img/tab-machine.png' },
		{ id: 'roasteries', key: 'tab.roasteries', img: '/img/tab-roastery.png' },
	];

	async function loadCoffees() {
		coffees = await api.coffees.list(undefined, currentPersonId);
	}

	async function loadGrinders() {
		grinders = await api.grinders.list();
	}

	async function loadBrewSetups() {
		brewSetups = await api.brewSetups.list();
	}

	async function loadRoasteries() {
		roasteriesList = await api.roasteries.list();
	}

	$effect(() => { currentPersonId; loadCoffees(); });
	$effect(() => { if (activeTab === 'grinding') loadGrinders(); });
	$effect(() => { if (activeTab === 'brewing') loadBrewSetups(); });
	$effect(() => { if (activeTab === 'roasteries') loadRoasteries(); });

	function selectCoffee(id: number) {
		coffeePanel = { type: 'detail', id };
	}

	async function onCoffeeCreated(id: number) {
		await loadCoffees();
		coffeePanel = { type: 'detail', id };
	}

	async function onCoffeeDeleted() {
		await loadCoffees();
		coffeePanel = { type: 'empty' };
	}

	// Grinder handlers
	function selectGrinder(id: number) {
		grinderPanel = { type: 'detail', id };
	}

	async function onGrinderCreated(id: number) {
		await loadGrinders();
		grinderPanel = { type: 'detail', id };
	}

	async function onGrinderUpdated() {
		await loadGrinders();
		// Re-select to refresh detail
		if (grinderPanel.type === 'detail') {
			grinderPanel = { ...grinderPanel };
		}
	}

	async function onGrinderDeleted() {
		await loadGrinders();
		grinderPanel = { type: 'empty' };
	}

	// Brew setup handlers
	function selectBrewSetup(id: number) {
		brewPanel = { type: 'detail', id };
	}

	function onMethodPicked(methodType: string, hasBasket: boolean) {
		brewPanel = { type: 'new', methodType, hasBasket };
	}

	async function onBrewSetupCreated(id: number) {
		await loadBrewSetups();
		brewPanel = { type: 'detail', id };
	}

	async function onBrewSetupUpdated() {
		await loadBrewSetups();
		if (brewPanel.type === 'detail') {
			brewPanel = { ...brewPanel };
		}
	}

	async function onBrewSetupDeleted() {
		await loadBrewSetups();
		brewPanel = { type: 'empty' };
	}

	// Roastery handlers
	function selectRoastery(id: number) {
		roasteryPanel = { type: 'detail', id };
	}

	async function onRoasteryCreated(id: number) {
		await loadRoasteries();
		roasteryPanel = { type: 'detail', id };
	}

	async function onRoasteryUpdated() {
		await loadRoasteries();
		if (roasteryPanel.type === 'detail') {
			roasteryPanel = { ...roasteryPanel };
		}
	}

	async function onRoasteryDeleted() {
		await loadRoasteries();
		roasteryPanel = { type: 'empty' };
	}

	function toggleLang() {
		lang.set(currentLang === 'en' ? 'uk' : 'en');
	}

	const appVersion = __APP_VERSION__;

	const selectedCoffeeId = $derived(coffeePanel.type === 'detail' ? coffeePanel.id : null);
	const selectedGrinderId = $derived(grinderPanel.type === 'detail' ? grinderPanel.id : null);
	const selectedBrewSetupId = $derived(brewPanel.type === 'detail' ? brewPanel.id : null);

	const selectedRoasteryId = $derived(roasteryPanel.type === 'detail' ? roasteryPanel.id : null);

	const selectedGrinder = $derived(
		selectedGrinderId != null ? grinders.find(g => g.id === selectedGrinderId) ?? null : null
	);
	const selectedBrewSetup = $derived(
		selectedBrewSetupId != null ? brewSetups.find(s => s.id === selectedBrewSetupId) ?? null : null
	);
	const selectedRoastery = $derived(
		selectedRoasteryId != null ? roasteriesList.find(r => r.id === selectedRoasteryId) ?? null : null
	);

	// Responsive: track if we're in mobile mode
	let innerWidth = $state(0);
	const isMobile = $derived(innerWidth < 768);

	// On mobile, detail panel is shown = sidebar hidden
	const showingDetail = $derived(
		(activeTab === 'coffee' && coffeePanel.type !== 'empty') ||
		(activeTab === 'grinding' && grinderPanel.type !== 'empty') ||
		(activeTab === 'brewing' && brewPanel.type !== 'empty') ||
		(activeTab === 'roasteries' && roasteryPanel.type !== 'empty')
	);

	function mobileBack() {
		if (activeTab === 'coffee') coffeePanel = { type: 'empty' };
		else if (activeTab === 'grinding') grinderPanel = { type: 'empty' };
		else if (activeTab === 'brewing') brewPanel = { type: 'empty' };
		else if (activeTab === 'roasteries') roasteryPanel = { type: 'empty' };
	}
</script>

<svelte:window bind:innerWidth />

<div class="flex flex-col h-screen overflow-hidden text-base">
	<!-- Top bar -->
	<header class="bg-card border-b border-stone-200 flex-shrink-0">
		<div class="flex items-center justify-between px-2 xl:px-5">
			<div class="flex items-center gap-2 xl:gap-8">
				<!-- Logo: icon only below xl -->
				<img src="/img/logo-text.png" alt="BeanBrain" class="self-stretch py-1 object-contain max-w-[80px] md:max-w-[120px] xl:max-w-[180px]" />

				<nav class="flex">
					{#each tabDefs as tab}
						<button
							onclick={() => activeTab = tab.id}
							class="flex items-center gap-1 xl:gap-3 px-2 md:px-4 xl:px-7 py-3 xl:py-5 text-lg font-medium transition-colors
								border-b-2 -mb-px
								{activeTab === tab.id
									? 'border-amber-600 text-amber-700'
									: 'border-transparent text-stone-400 hover:text-stone-600'}"
						>
							<img src={tab.img} alt="" class="w-7 h-7 md:w-9 md:h-9 xl:w-12 xl:h-12 {activeTab === tab.id ? 'opacity-90' : 'opacity-40'}" />
							<span class="hidden xl:inline">{$t(tab.key)}</span>
						</button>
					{/each}
				</nav>
			</div>

			<div class="flex items-center gap-2 xl:gap-3">
				<span class="hidden md:inline text-xs text-stone-300 font-mono">v{appVersion}</span>
				<PersonSwitcher onChange={loadCoffees} />
				<button
					onclick={toggleLang}
					class="flex items-center gap-1.5 px-2 xl:px-3 py-2 rounded-lg text-sm font-medium
						bg-card-inset hover:bg-parchment transition-colors text-stone-500"
					title="Switch language"
				>
					{#if currentLang === 'en'}
						<span class="text-lg leading-none">🇬🇧</span>
						<span class="hidden xl:inline">EN</span>
					{:else}
						<span class="text-lg leading-none">🇺🇦</span>
						<span class="hidden xl:inline">UA</span>
					{/if}
				</button>
			</div>
		</div>
	</header>

	<!-- Content -->
	<div class="flex flex-1 overflow-hidden">
		{#if activeTab === 'coffee'}
			{#if !isMobile || !showingDetail}
				<CoffeeSidebar
					{coffees}
					selectedId={selectedCoffeeId}
					onSelect={selectCoffee}
					onAdd={() => coffeePanel = { type: 'new' }}
					onRefresh={loadCoffees}
				/>
			{/if}
			{#if !isMobile || showingDetail}
				<div class="flex-1 overflow-y-auto bg-parchment" style="background-image: url('/img/bg-pattern.png'); background-repeat: repeat;">
					{#if coffeePanel.type === 'empty'}
						<EmptyState img="choose-coffee.png" title={$t('empty.title')} subtitle={$t('empty.subtitle')} />
					{:else if coffeePanel.type === 'detail'}
						<CoffeeDetail coffeeId={coffeePanel.id} onDeleted={onCoffeeDeleted} onUpdated={loadCoffees} onBack={isMobile ? mobileBack : () => coffeePanel = { type: 'empty' }} />
					{:else if coffeePanel.type === 'new'}
						<AddCoffeePanel onCreated={onCoffeeCreated} onCancel={isMobile ? mobileBack : () => coffeePanel = { type: 'empty' }} />
					{/if}
				</div>
			{/if}

		{:else if activeTab === 'grinding'}
			{#if !isMobile || !showingDetail}
				<GrindingSidebar
					{grinders}
					selectedId={selectedGrinderId}
					onSelect={selectGrinder}
					onAdd={() => grinderPanel = { type: 'new' }}
				/>
			{/if}
			{#if !isMobile || showingDetail}
				<div class="flex-1 overflow-y-auto bg-parchment" style="background-image: url('/img/bg-pattern.png'); background-repeat: repeat;">
					{#if grinderPanel.type === 'empty'}
						<EmptyState img="many-grinders.png" title={$t('grinding.select')} />
					{:else if grinderPanel.type === 'detail' && selectedGrinder}
						<GrinderDetail grinder={selectedGrinder} onUpdated={onGrinderUpdated} onDeleted={onGrinderDeleted} onBack={isMobile ? mobileBack : () => grinderPanel = { type: 'empty' }} />
					{:else if grinderPanel.type === 'new'}
						<AddGrinderPanel onCreated={onGrinderCreated} onCancel={isMobile ? mobileBack : () => grinderPanel = { type: 'empty' }} />
					{/if}
				</div>
			{/if}

		{:else if activeTab === 'brewing'}
			{#if !isMobile || !showingDetail}
				<BrewingSidebar
					{brewSetups}
					selectedId={selectedBrewSetupId}
					onSelect={selectBrewSetup}
					onAdd={() => brewPanel = { type: 'pick_method' }}
				/>
			{/if}
			{#if !isMobile || showingDetail}
				<div class="flex-1 overflow-y-auto bg-parchment" style="background-image: url('/img/bg-pattern.png'); background-repeat: repeat;">
					{#if brewPanel.type === 'empty'}
						<EmptyState img="many-brewmethods.png" title={$t('brewing.select')} />
					{:else if brewPanel.type === 'detail' && selectedBrewSetup}
						<BrewSetupDetail brewSetup={selectedBrewSetup} onUpdated={onBrewSetupUpdated} onDeleted={onBrewSetupDeleted} onBack={isMobile ? mobileBack : () => brewPanel = { type: 'empty' }} />
					{:else if brewPanel.type === 'pick_method'}
						<BrewMethodPicker onPicked={onMethodPicked} onCancel={isMobile ? mobileBack : () => brewPanel = { type: 'empty' }} />
					{:else if brewPanel.type === 'new'}
						<AddBrewSetupPanel methodType={brewPanel.methodType} hasBasket={brewPanel.hasBasket} onCreated={onBrewSetupCreated} onCancel={isMobile ? mobileBack : () => brewPanel = { type: 'empty' }} />
					{/if}
				</div>
			{/if}

		{:else if activeTab === 'roasteries'}
			{#if !isMobile || !showingDetail}
				<RoasterySidebar
					roasteries={roasteriesList}
					selectedId={selectedRoasteryId}
					onSelect={selectRoastery}
					onAdd={() => roasteryPanel = { type: 'new' }}
				/>
			{/if}
			{#if !isMobile || showingDetail}
				<div class="flex-1 overflow-y-auto bg-parchment" style="background-image: url('/img/bg-pattern.png'); background-repeat: repeat;">
					{#if roasteryPanel.type === 'empty'}
						<EmptyState img="many-roasteries.png" title={$t('roastery.select')} />
					{:else if roasteryPanel.type === 'detail' && selectedRoastery}
						<RoasteryDetail roastery={selectedRoastery} onUpdated={onRoasteryUpdated} onDeleted={onRoasteryDeleted} onBack={isMobile ? mobileBack : () => roasteryPanel = { type: 'empty' }} />
					{:else if roasteryPanel.type === 'new'}
						<AddRoasteryPanel onCreated={onRoasteryCreated} onCancel={isMobile ? mobileBack : () => roasteryPanel = { type: 'empty' }} />
					{/if}
				</div>
			{/if}
		{/if}
	</div>
</div>
