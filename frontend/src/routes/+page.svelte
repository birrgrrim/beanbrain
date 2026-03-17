<script lang="ts">
	import { api, type CoffeeListItem } from '$lib/api';
	import CoffeeSidebar from '$lib/components/CoffeeSidebar.svelte';
	import CoffeeDetail from '$lib/components/CoffeeDetail.svelte';
	import AddCoffeePanel from '$lib/components/AddCoffeePanel.svelte';
	import EquipmentPanel from '$lib/components/EquipmentPanel.svelte';
	import Icons from '$lib/components/Icons.svelte';

	type Panel = { type: 'empty' } | { type: 'coffee'; id: number } | { type: 'new' } | { type: 'settings' };

	let coffees = $state<CoffeeListItem[]>([]);
	let panel = $state<Panel>({ type: 'empty' });

	async function loadCoffees() {
		coffees = await api.coffees.list();
	}

	$effect(() => { loadCoffees(); });

	function selectCoffee(id: number) {
		panel = { type: 'coffee', id };
	}

	function addCoffee() {
		panel = { type: 'new' };
	}

	function showSettings() {
		panel = { type: 'settings' };
	}

	async function onCoffeeCreated(id: number) {
		await loadCoffees();
		panel = { type: 'coffee', id };
	}

	async function onCoffeeDeleted() {
		await loadCoffees();
		panel = { type: 'empty' };
	}

	const selectedId = $derived(panel.type === 'coffee' ? panel.id : null);
</script>

<div class="flex h-screen overflow-hidden">
	<!-- Sidebar -->
	<div class="flex flex-col">
		<CoffeeSidebar
			{coffees}
			{selectedId}
			onSelect={selectCoffee}
			onAdd={addCoffee}
			onRefresh={loadCoffees}
		/>
		<!-- Bottom nav -->
		<div class="w-80 border-r border-stone-200 bg-white border-t border-t-stone-100 p-2 flex-shrink-0">
			<button
				onclick={showSettings}
				class="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-stone-400
					hover:bg-stone-50 hover:text-stone-600 transition-colors
					{panel.type === 'settings' ? 'bg-stone-50 text-stone-600' : ''}"
			>
				<Icons icon="settings" size={16} />
				Settings
			</button>
		</div>
	</div>

	<!-- Content panel -->
	<div class="flex-1 overflow-y-auto bg-[#faf8f5]">
		{#if panel.type === 'empty'}
			<div class="flex flex-col items-center justify-center h-full text-center">
				<Icons icon="bean" size={48} className="text-stone-200 mb-3" />
				<p class="text-stone-300 text-lg" style="font-family: 'DM Serif Display', serif;">Select a coffee</p>
				<p class="text-stone-200 text-sm mt-1">or add a new one to get started</p>
			</div>
		{:else if panel.type === 'coffee'}
			<CoffeeDetail coffeeId={panel.id} onDeleted={onCoffeeDeleted} />
		{:else if panel.type === 'new'}
			<AddCoffeePanel onCreated={onCoffeeCreated} onCancel={() => panel = { type: 'empty' }} />
		{:else if panel.type === 'settings'}
			<EquipmentPanel />
		{/if}
	</div>
</div>
