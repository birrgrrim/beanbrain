<script lang="ts">
	import { api, type CoffeeListItem } from '$lib/api';
	import { lang, type Lang } from '$lib/lang';
	import { t } from '$lib/i18n';
	import CoffeeSidebar from '$lib/components/CoffeeSidebar.svelte';
	import CoffeeDetail from '$lib/components/CoffeeDetail.svelte';
	import AddCoffeePanel from '$lib/components/AddCoffeePanel.svelte';
	import GrindersPanel from '$lib/components/GrindersPanel.svelte';
	import PersonsPanel from '$lib/components/PersonsPanel.svelte';
	import Icons from '$lib/components/Icons.svelte';

	type Tab = 'coffee' | 'grinders' | 'persons';
	type CoffeePanel = { type: 'empty' } | { type: 'detail'; id: number } | { type: 'new' };

	let activeTab = $state<Tab>('coffee');
	let coffees = $state<CoffeeListItem[]>([]);
	let coffeePanel = $state<CoffeePanel>({ type: 'empty' });
	let currentLang = $state<Lang>('en');

	lang.subscribe(v => currentLang = v);

	const tabDefs: { id: Tab; key: string; icon: 'bean' | 'grinder' | 'cup' }[] = [
		{ id: 'coffee', key: 'tab.coffee', icon: 'bean' },
		{ id: 'grinders', key: 'tab.grinders', icon: 'grinder' },
		{ id: 'persons', key: 'tab.persons', icon: 'cup' },
	];

	async function loadCoffees() {
		coffees = await api.coffees.list();
	}

	$effect(() => { loadCoffees(); });

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

	function toggleLang() {
		lang.set(currentLang === 'en' ? 'uk' : 'en');
	}

	const selectedId = $derived(coffeePanel.type === 'detail' ? coffeePanel.id : null);
</script>

<div class="flex flex-col h-screen overflow-hidden">
	<!-- Top bar -->
	<header class="bg-white border-b border-stone-200 flex-shrink-0">
		<div class="flex items-center justify-between px-4">
			<div class="flex items-center gap-6">
				<h1 class="text-lg font-bold text-stone-800 py-3" style="font-family: 'DM Serif Display', serif;">
					BeanBrain
				</h1>

				<nav class="flex">
					{#each tabDefs as tab}
						<button
							onclick={() => activeTab = tab.id}
							class="flex items-center gap-1.5 px-4 py-3 text-sm font-medium transition-colors
								border-b-2 -mb-px
								{activeTab === tab.id
									? 'border-amber-600 text-amber-700'
									: 'border-transparent text-stone-400 hover:text-stone-600'}"
						>
							<Icons icon={tab.icon} size={15}
								className={activeTab === tab.id ? 'text-amber-600' : 'text-stone-300'} />
							{$t(tab.key)}
						</button>
					{/each}
				</nav>
			</div>

			<button
				onclick={toggleLang}
				class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-medium
					bg-stone-50 hover:bg-stone-100 transition-colors text-stone-500"
				title="Switch language"
			>
				{#if currentLang === 'en'}
					<span class="text-base leading-none">🇬🇧</span>
					<span>EN</span>
				{:else}
					<span class="text-base leading-none">🇺🇦</span>
					<span>UA</span>
				{/if}
			</button>
		</div>
	</header>

	<!-- Content -->
	<div class="flex flex-1 overflow-hidden">
		{#if activeTab === 'coffee'}
			<CoffeeSidebar
				{coffees}
				{selectedId}
				onSelect={selectCoffee}
				onAdd={() => coffeePanel = { type: 'new' }}
				onRefresh={loadCoffees}
			/>
			<div class="flex-1 overflow-y-auto bg-[#faf8f5]">
				{#if coffeePanel.type === 'empty'}
					<div class="flex flex-col items-center justify-center h-full text-center">
						<Icons icon="bean" size={48} className="text-stone-200 mb-3" />
						<p class="text-stone-300 text-lg" style="font-family: 'DM Serif Display', serif;">{$t('empty.title')}</p>
						<p class="text-stone-200 text-sm mt-1">{$t('empty.subtitle')}</p>
					</div>
				{:else if coffeePanel.type === 'detail'}
					<CoffeeDetail coffeeId={coffeePanel.id} onDeleted={onCoffeeDeleted} />
				{:else if coffeePanel.type === 'new'}
					<AddCoffeePanel onCreated={onCoffeeCreated} onCancel={() => coffeePanel = { type: 'empty' }} />
				{/if}
			</div>
		{:else if activeTab === 'grinders'}
			<div class="flex-1 overflow-y-auto bg-[#faf8f5]">
				<GrindersPanel />
			</div>
		{:else if activeTab === 'persons'}
			<div class="flex-1 overflow-y-auto bg-[#faf8f5]">
				<PersonsPanel />
			</div>
		{/if}
	</div>
</div>
