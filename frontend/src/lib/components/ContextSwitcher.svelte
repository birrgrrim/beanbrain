<script lang="ts">
	import { api, type Taster, type Grinder, type BrewSetup } from '$lib/api';
	import { activePerson } from '$lib/personStore';
	import { activeGrinder, activeBrewSetup } from '$lib/contextStore';
	import { t } from '$lib/i18n';
	import SwitcherPopover from './SwitcherPopover.svelte';

	let { onChange }: { onChange: () => void } = $props();

	let tasters = $state<Taster[]>([]);
	let grinders = $state<Grinder[]>([]);
	let brewSetups = $state<BrewSetup[]>([]);

	let openPanel = $state<'person' | 'grinder' | 'brew' | null>(null);

	let currentPersonId = $state<number | null>(null);
	let currentGrinderId = $state<number | null>(null);
	let currentBrewSetupId = $state<number | null>(null);

	activePerson.subscribe(v => currentPersonId = v);
	activeGrinder.subscribe(v => currentGrinderId = v);
	activeBrewSetup.subscribe(v => currentBrewSetupId = v);

	async function loadAll() {
		[tasters, grinders, brewSetups] = await Promise.all([
			api.tasters.list(),
			api.grinders.list(),
			api.brewSetups.list(),
		]);

		// Auto-select defaults if nothing stored
		if (currentGrinderId === null || !grinders.some(g => g.id === currentGrinderId)) {
			const def = grinders.find(g => g.is_default) ?? grinders[0];
			if (def) activeGrinder.set(def.id);
		}
		if (currentBrewSetupId === null || !brewSetups.some(s => s.id === currentBrewSetupId)) {
			const def = brewSetups.find(s => s.is_default) ?? brewSetups[0];
			if (def) activeBrewSetup.set(def.id);
		}
		if (currentPersonId !== null && !tasters.some(t => t.id === currentPersonId)) {
			activePerson.set(null);
		}
	}

	$effect(() => { loadAll(); });

	function selectPerson(id: number | null) {
		activePerson.set(id);
		openPanel = null;
		onChange();
	}

	function selectGrinder(id: number | null) {
		if (id !== null) activeGrinder.set(id);
		openPanel = null;
		onChange();
	}

	function selectBrewSetup(id: number | null) {
		if (id !== null) activeBrewSetup.set(id);
		openPanel = null;
		onChange();
	}

	async function addPerson(name: string) {
		const created = await api.tasters.create(name);
		await loadAll();
		selectPerson(created.id);
	}

	async function addGrinder(name: string) {
		const created = await api.grinders.create({ manufacturer: name });
		await loadAll();
		selectGrinder(created.id);
	}

	async function addBrewSetup(name: string) {
		const created = await api.brewSetups.create({ method_type: 'espresso', manufacturer: name });
		await loadAll();
		selectBrewSetup(created.id);
	}

	async function removePerson(id: number) {
		await api.tasters.delete(id);
		if (currentPersonId === id) activePerson.set(null);
		await loadAll();
		onChange();
	}

	async function removeGrinder(id: number) {
		await api.grinders.delete(id);
		if (currentGrinderId === id) {
			const next = grinders.find(g => g.id !== id);
			activeGrinder.set(next?.id ?? null);
		}
		await loadAll();
		onChange();
	}

	async function removeBrewSetup(id: number) {
		await api.brewSetups.delete(id);
		if (currentBrewSetupId === id) {
			const next = brewSetups.find(s => s.id !== id);
			activeBrewSetup.set(next?.id ?? null);
		}
		await loadAll();
		onChange();
	}

	const currentPerson = $derived(tasters.find(t => t.id === currentPersonId));
	const currentGrinder = $derived(grinders.find(g => g.id === currentGrinderId));
	const currentBrewSetup = $derived(brewSetups.find(s => s.id === currentBrewSetupId));

	const personItems = $derived(tasters.map(t => ({
		id: t.id,
		label: t.name,
		icon: '/img/tab-person.png',
	})));

	const grinderItems = $derived(grinders.map(g => ({
		id: g.id,
		label: `${g.manufacturer}${g.model ? ` ${g.model}` : ''}`,
		sublabel: g.range_max ? `${g.range_min}–${g.range_max} step ${g.step}` : `step ${g.step}`,
		icon: `/img/grinder-${g.kind === 'manual' ? 'manual' : 'auto'}.png`,
	})));

	const brewItems = $derived(brewSetups.map(s => ({
		id: s.id,
		label: `${s.manufacturer}${s.model ? ` ${s.model}` : ''}`,
		sublabel: s.basket_grams ? `${s.basket_grams}g` : undefined,
		icon: `/img/method-${s.method_type}.png`,
	})));

	function toggle(panel: 'person' | 'grinder' | 'brew') {
		openPanel = openPanel === panel ? null : panel;
	}

	function handleClickOutside(event: MouseEvent) {
		const target = event.target as HTMLElement;
		if (!target.closest('.context-switcher')) {
			openPanel = null;
		}
	}
</script>

<svelte:window onclick={handleClickOutside} />

<div class="context-switcher flex items-center gap-1.5">
	<!-- Person -->
	<div class="relative">
		<button
			onclick={() => toggle('person')}
			class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-sm font-medium
				hover:bg-parchment transition-colors
				{openPanel === 'person' ? 'bg-parchment' : 'bg-card-inset'} text-stone-500"
			title={currentPerson?.name ?? $t('person.everyone')}
		>
			<img src="/img/tab-person.png" alt="" class="w-6 h-6 opacity-60" />
			<span class="max-w-[80px] truncate hidden md:inline">{currentPerson?.name ?? $t('person.everyone')}</span>
		</button>
		{#if openPanel === 'person'}
			<div class="absolute right-0 top-full mt-1">
				<SwitcherPopover
					items={personItems}
					activeId={currentPersonId}
					everyoneLabel={$t('person.everyone')}
					addPlaceholder={$t('persons.add_placeholder')}
					addLabel={$t('persons.add')}
					onSelect={selectPerson}
					onAdd={addPerson}
					onRemove={removePerson}
				/>
			</div>
		{/if}
	</div>

	<!-- Grinder -->
	<div class="relative">
		<button
			onclick={() => toggle('grinder')}
			class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-sm font-medium
				hover:bg-parchment transition-colors
				{openPanel === 'grinder' ? 'bg-parchment' : 'bg-card-inset'} text-stone-500"
			title={currentGrinder ? `${currentGrinder.manufacturer}${currentGrinder.model ? ` ${currentGrinder.model}` : ''}` : 'Grinder'}
		>
			<img src="/img/grinder-{currentGrinder?.kind === 'manual' ? 'manual' : 'auto'}.png" alt="" class="w-6 h-6 opacity-60" />
			<span class="max-w-[80px] truncate hidden lg:inline">{currentGrinder?.manufacturer ?? '—'}</span>
		</button>
		{#if openPanel === 'grinder'}
			<div class="absolute right-0 top-full mt-1">
				<SwitcherPopover
					items={grinderItems}
					activeId={currentGrinderId}
					addPlaceholder={$t('grinding.manufacturer_placeholder')}
					addLabel={$t('grinding.add')}
					onSelect={selectGrinder}
					onAdd={addGrinder}
					onRemove={removeGrinder}
				/>
			</div>
		{/if}
	</div>

	<!-- Brew Setup -->
	<div class="relative">
		<button
			onclick={() => toggle('brew')}
			class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-sm font-medium
				hover:bg-parchment transition-colors
				{openPanel === 'brew' ? 'bg-parchment' : 'bg-card-inset'} text-stone-500"
			title={currentBrewSetup ? `${currentBrewSetup.manufacturer}${currentBrewSetup.model ? ` ${currentBrewSetup.model}` : ''}` : 'Brew'}
		>
			<img src="/img/method-{currentBrewSetup?.method_type ?? 'espresso'}.png" alt="" class="w-6 h-6 opacity-60" />
			<span class="max-w-[80px] truncate hidden lg:inline">{currentBrewSetup?.manufacturer ?? '—'}</span>
		</button>
		{#if openPanel === 'brew'}
			<div class="absolute right-0 top-full mt-1">
				<SwitcherPopover
					items={brewItems}
					activeId={currentBrewSetupId}
					addPlaceholder={$t('brewing.manufacturer_placeholder')}
					addLabel={$t('brewing.add')}
					onSelect={selectBrewSetup}
					onAdd={addBrewSetup}
					onRemove={removeBrewSetup}
				/>
			</div>
		{/if}
	</div>
</div>
