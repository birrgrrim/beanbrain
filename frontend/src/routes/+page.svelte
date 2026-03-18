<script lang="ts">
	import { api, type CoffeeListItem, type Grinder, type BrewSetup } from '$lib/api';
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
	import PersonSwitcher from '$lib/components/PersonSwitcher.svelte';

	type Tab = 'coffee' | 'grinding' | 'brewing';
	type CoffeePanel = { type: 'empty' } | { type: 'detail'; id: number } | { type: 'new' };
	type GrinderPanel = { type: 'empty' } | { type: 'detail'; id: number } | { type: 'new' };
	type BrewPanel = { type: 'empty' } | { type: 'detail'; id: number } | { type: 'pick_method' } | { type: 'new'; methodType: string; hasBasket: boolean };

	let activeTab = $state<Tab>('coffee');
	let coffees = $state<CoffeeListItem[]>([]);
	let coffeePanel = $state<CoffeePanel>({ type: 'empty' });

	let grinders = $state<Grinder[]>([]);
	let grinderPanel = $state<GrinderPanel>({ type: 'empty' });

	let brewSetups = $state<BrewSetup[]>([]);
	let brewPanel = $state<BrewPanel>({ type: 'empty' });

	let currentLang = $state<Lang>('en');
	let currentPersonId = $state<number | null>(null);

	lang.subscribe(v => currentLang = v);
	activePerson.subscribe(v => currentPersonId = v);

	const tabDefs: { id: Tab; key: string; img: string }[] = [
		{ id: 'coffee', key: 'tab.coffee', img: '/img/tab-coffee.png' },
		{ id: 'grinding', key: 'tab.grinding', img: '/img/tab-grinder.png' },
		{ id: 'brewing', key: 'tab.brewing', img: '/img/tab-machine.png' },
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

	$effect(() => { currentPersonId; loadCoffees(); });
	$effect(() => { if (activeTab === 'grinding') loadGrinders(); });
	$effect(() => { if (activeTab === 'brewing') loadBrewSetups(); });

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

	function toggleLang() {
		lang.set(currentLang === 'en' ? 'uk' : 'en');
	}

	const selectedCoffeeId = $derived(coffeePanel.type === 'detail' ? coffeePanel.id : null);
	const selectedGrinderId = $derived(grinderPanel.type === 'detail' ? grinderPanel.id : null);
	const selectedBrewSetupId = $derived(brewPanel.type === 'detail' ? brewPanel.id : null);

	const selectedGrinder = $derived(
		selectedGrinderId != null ? grinders.find(g => g.id === selectedGrinderId) ?? null : null
	);
	const selectedBrewSetup = $derived(
		selectedBrewSetupId != null ? brewSetups.find(s => s.id === selectedBrewSetupId) ?? null : null
	);
</script>

<div class="flex flex-col h-screen overflow-hidden text-base">
	<!-- Top bar -->
	<header class="bg-card border-b border-stone-200 flex-shrink-0">
		<div class="flex items-center justify-between px-5">
			<div class="flex items-center gap-8">
				<div class="flex items-center gap-3 py-4">
					<img src="/img/logo.png" alt="BeanBrain" class="h-12 w-12" />
					<span class="text-3xl font-bold text-stone-800" style="font-family: 'DM Serif Display', serif;">BeanBrain</span>
				</div>

				<nav class="flex">
					{#each tabDefs as tab}
						<button
							onclick={() => activeTab = tab.id}
							class="flex items-center gap-3 px-7 py-5 text-lg font-medium transition-colors
								border-b-2 -mb-px
								{activeTab === tab.id
									? 'border-amber-600 text-amber-700'
									: 'border-transparent text-stone-400 hover:text-stone-600'}"
						>
							<img src={tab.img} alt="" class="w-8 h-8 {activeTab === tab.id ? 'opacity-90' : 'opacity-40'}" />
							{$t(tab.key)}
						</button>
					{/each}
				</nav>
			</div>

			<div class="flex items-center gap-3">
				<PersonSwitcher onChange={loadCoffees} />
				<button
					onclick={toggleLang}
					class="flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium
						bg-card-inset hover:bg-parchment transition-colors text-stone-500"
					title="Switch language"
				>
					{#if currentLang === 'en'}
						<span class="text-lg leading-none">🇬🇧</span>
						<span>EN</span>
					{:else}
						<span class="text-lg leading-none">🇺🇦</span>
						<span>UA</span>
					{/if}
				</button>
			</div>
		</div>
	</header>

	<!-- Content -->
	<div class="flex flex-1 overflow-hidden">
		{#if activeTab === 'coffee'}
			<CoffeeSidebar
				{coffees}
				selectedId={selectedCoffeeId}
				onSelect={selectCoffee}
				onAdd={() => coffeePanel = { type: 'new' }}
				onRefresh={loadCoffees}
			/>
			<div class="flex-1 overflow-y-auto bg-parchment" style="background-image: url('/img/bg-pattern.png'); background-repeat: repeat;">
				{#if coffeePanel.type === 'empty'}
					<div class="flex flex-col items-center justify-center h-full text-center">
						<div class="rounded-full bg-parchment p-8 mb-4"
							style="box-shadow: 0 0 40px 20px var(--color-parchment);">
							<img src="/img/choose-coffee.png" alt="" class="opacity-70" style="max-width: 220px;" />
						</div>
						<p class="text-stone-500 text-2xl" style="font-family: 'DM Serif Display', serif;">{$t('empty.title')}</p>
						<p class="text-stone-400 text-base mt-2">{$t('empty.subtitle')}</p>
					</div>
				{:else if coffeePanel.type === 'detail'}
					<CoffeeDetail coffeeId={coffeePanel.id} onDeleted={onCoffeeDeleted} onUpdated={loadCoffees} onBack={() => coffeePanel = { type: 'empty' }} />
				{:else if coffeePanel.type === 'new'}
					<AddCoffeePanel onCreated={onCoffeeCreated} onCancel={() => coffeePanel = { type: 'empty' }} />
				{/if}
			</div>

		{:else if activeTab === 'grinding'}
			<GrindingSidebar
				{grinders}
				selectedId={selectedGrinderId}
				onSelect={selectGrinder}
				onAdd={() => grinderPanel = { type: 'new' }}
			/>
			<div class="flex-1 overflow-y-auto bg-parchment" style="background-image: url('/img/bg-pattern.png'); background-repeat: repeat;">
				{#if grinderPanel.type === 'empty'}
					<div class="flex flex-col items-center justify-center h-full text-center">
						<div class="rounded-full bg-parchment p-8 mb-4"
							style="box-shadow: 0 0 40px 20px var(--color-parchment);">
							<img src="/img/many-grinders.png" alt="" class="opacity-70" style="max-width: 220px;" />
						</div>
						<p class="text-stone-500 text-2xl" style="font-family: 'DM Serif Display', serif;">{$t('grinding.select')}</p>
					</div>
				{:else if grinderPanel.type === 'detail' && selectedGrinder}
					<GrinderDetail grinder={selectedGrinder} onUpdated={onGrinderUpdated} onDeleted={onGrinderDeleted} onBack={() => grinderPanel = { type: 'empty' }} />
				{:else if grinderPanel.type === 'new'}
					<AddGrinderPanel onCreated={onGrinderCreated} onCancel={() => grinderPanel = { type: 'empty' }} />
				{/if}
			</div>

		{:else if activeTab === 'brewing'}
			<BrewingSidebar
				{brewSetups}
				selectedId={selectedBrewSetupId}
				onSelect={selectBrewSetup}
				onAdd={() => brewPanel = { type: 'pick_method' }}
			/>
			<div class="flex-1 overflow-y-auto bg-parchment" style="background-image: url('/img/bg-pattern.png'); background-repeat: repeat;">
				{#if brewPanel.type === 'empty'}
					<div class="flex flex-col items-center justify-center h-full text-center">
						<div class="rounded-full bg-parchment p-8 mb-4"
							style="box-shadow: 0 0 40px 20px var(--color-parchment);">
							<img src="/img/many-brewmethods.png" alt="" class="opacity-70" style="max-width: 220px;" />
						</div>
						<p class="text-stone-500 text-2xl" style="font-family: 'DM Serif Display', serif;">{$t('brewing.select')}</p>
					</div>
				{:else if brewPanel.type === 'detail' && selectedBrewSetup}
					<BrewSetupDetail brewSetup={selectedBrewSetup} onUpdated={onBrewSetupUpdated} onDeleted={onBrewSetupDeleted} onBack={() => brewPanel = { type: 'empty' }} />
				{:else if brewPanel.type === 'pick_method'}
					<BrewMethodPicker onPicked={onMethodPicked} onCancel={() => brewPanel = { type: 'empty' }} />
				{:else if brewPanel.type === 'new'}
					<AddBrewSetupPanel methodType={brewPanel.methodType} hasBasket={brewPanel.hasBasket} onCreated={onBrewSetupCreated} onCancel={() => brewPanel = { type: 'empty' }} />
				{/if}
			</div>
		{/if}
	</div>
</div>
