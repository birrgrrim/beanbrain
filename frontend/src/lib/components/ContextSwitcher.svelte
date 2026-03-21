<script lang="ts">
	import { api, type Taster, type Grinder, type BrewSetup, type BrewMethodType } from '$lib/api';
	import { activePerson } from '$lib/personStore';
	import { activeGrinder, activeBrewSetup } from '$lib/contextStore';
	import { t } from '$lib/i18n';
	import SwitcherPopover from './SwitcherPopover.svelte';
	import EditDialog from './EditDialog.svelte';

	let { onChange }: { onChange: () => void } = $props();

	let tasters = $state<Taster[]>([]);
	let grinders = $state<Grinder[]>([]);
	let brewSetups = $state<BrewSetup[]>([]);
	let brewMethodTypes = $state<BrewMethodType[]>([]);

	let openPanel = $state<'person' | 'grinder' | 'brew' | null>(null);

	type DialogState =
		| null
		| { type: 'person'; mode: 'add' }
		| { type: 'person'; mode: 'edit'; item: Taster }
		| { type: 'grinder'; mode: 'add' }
		| { type: 'grinder'; mode: 'edit'; item: Grinder }
		| { type: 'brew'; mode: 'add' }
		| { type: 'brew'; mode: 'edit'; item: BrewSetup };

	let dialogState = $state<DialogState>(null);

	let currentPersonId = $state<number | null>(null);
	let currentGrinderId = $state<number | null>(null);
	let currentBrewSetupId = $state<number | null>(null);

	activePerson.subscribe(v => currentPersonId = v);
	activeGrinder.subscribe(v => currentGrinderId = v);
	activeBrewSetup.subscribe(v => currentBrewSetupId = v);

	async function loadAll() {
		[tasters, grinders, brewSetups, brewMethodTypes] = await Promise.all([
			api.tasters.list(),
			api.grinders.list(),
			api.brewSetups.list(),
			api.brewMethodTypes.list(),
		]);

		if (currentGrinderId === null || !grinders.some(g => g.id === currentGrinderId)) {
			const def = grinders[0];
			if (def) activeGrinder.set(def.id);
		}
		if (currentBrewSetupId === null || !brewSetups.some(s => s.id === currentBrewSetupId)) {
			const def = brewSetups[0];
			if (def) activeBrewSetup.set(def.id);
		}
		if (currentPersonId === null || !tasters.some(t => t.id === currentPersonId)) {
			const def = tasters[0];
			if (def) activePerson.set(def.id);
		}
	}

	$effect(() => { loadAll(); });

	function selectPerson(id: number | null) {
		if (id !== null) activePerson.set(id);
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

	function openAdd(type: 'person' | 'grinder' | 'brew') {
		openPanel = null;
		dialogState = { type, mode: 'add' };
	}

	function openEditPerson(id: number) {
		openPanel = null;
		const item = tasters.find(t => t.id === id);
		if (item) dialogState = { type: 'person', mode: 'edit', item };
	}

	function openEditGrinder(id: number) {
		openPanel = null;
		const item = grinders.find(g => g.id === id);
		if (item) dialogState = { type: 'grinder', mode: 'edit', item };
	}

	function openEditBrewSetup(id: number) {
		openPanel = null;
		const item = brewSetups.find(s => s.id === id);
		if (item) dialogState = { type: 'brew', mode: 'edit', item };
	}

	async function onDialogSaved() {
		dialogState = null;
		await loadAll();
		onChange();
	}

	async function onDialogDeleted() {
		const ds = dialogState;
		dialogState = null;
		if (ds?.type === 'person' && ds.mode === 'edit' && currentPersonId === ds.item.id) {
			activePerson.set(null);
		} else if (ds?.type === 'grinder' && ds.mode === 'edit' && currentGrinderId === ds.item.id) {
			activeGrinder.set(null);
		} else if (ds?.type === 'brew' && ds.mode === 'edit' && currentBrewSetupId === ds.item.id) {
			activeBrewSetup.set(null);
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
		icon: t.avatar ?? '/img/avatar-person-1.png',
		isCustomAvatar: !!t.avatar,
	})));

	const grinderItems = $derived(grinders.map(g => ({
		id: g.id,
		label: `${g.manufacturer}${g.model ? ` ${g.model}` : ''}`,
		sublabel: g.range_max ? `${g.range_min}–${g.range_max} step ${g.step}` : `step ${g.step}`,
		icon: g.avatar ?? `/img/grinder-${g.kind === 'manual' ? 'manual' : 'auto'}.png`,
		isCustomAvatar: !!g.avatar,
	})));

	const brewItems = $derived(brewSetups.map(s => ({
		id: s.id,
		label: `${s.manufacturer}${s.model ? ` ${s.model}` : ''}`,
		sublabel: s.basket_grams ? `${s.basket_grams}g` : undefined,
		icon: s.avatar ?? `/img/method-${s.method_type}.png`,
		isCustomAvatar: !!s.avatar,
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

<div class="context-switcher flex items-center gap-2">
	<!-- Person -->
	<div class="relative">
		<button
			onclick={() => toggle('person')}
			class="w-10 h-10 rounded-xl overflow-hidden border-2 transition-colors hover:border-amber-300
				{openPanel === 'person' ? 'border-amber-400 shadow-sm' : 'border-stone-200'}"
			title={currentPerson?.name ?? $t('person.everyone')}
		>
			<img src={currentPerson?.avatar ?? '/img/avatar-person-1.png'} alt="" class="w-full h-full object-cover" />
		</button>
		{#if openPanel === 'person'}
			<div class="absolute right-0 top-full mt-1">
				<SwitcherPopover
					items={personItems}
					activeId={currentPersonId}
					addLabel={$t('persons.add')}
					onSelect={selectPerson}
					onAdd={() => openAdd('person')}
					onEdit={openEditPerson}
				/>
			</div>
		{/if}
	</div>

	<!-- Grinder -->
	<div class="relative">
		<button
			onclick={() => toggle('grinder')}
			class="w-10 h-10 rounded-xl overflow-hidden border-2 transition-colors hover:border-amber-300
				{openPanel === 'grinder' ? 'border-amber-400 shadow-sm' : 'border-stone-200'}"
			title={currentGrinder ? `${currentGrinder.manufacturer}${currentGrinder.model ? ` ${currentGrinder.model}` : ''}` : 'Grinder'}
		>
			<img src={currentGrinder?.avatar ?? `/img/grinder-${currentGrinder?.kind === 'manual' ? 'manual' : 'auto'}.png`} alt="" class="w-full h-full object-cover" />
		</button>
		{#if openPanel === 'grinder'}
			<div class="absolute right-0 top-full mt-1">
				<SwitcherPopover
					items={grinderItems}
					activeId={currentGrinderId}
					addLabel={$t('grinding.add')}
					onSelect={selectGrinder}
					onAdd={() => openAdd('grinder')}
					onEdit={openEditGrinder}
				/>
			</div>
		{/if}
	</div>

	<!-- Brew Setup -->
	<div class="relative">
		<button
			onclick={() => toggle('brew')}
			class="w-10 h-10 rounded-xl overflow-hidden border-2 transition-colors hover:border-amber-300
				{openPanel === 'brew' ? 'border-amber-400 shadow-sm' : 'border-stone-200'}"
			title={currentBrewSetup ? `${currentBrewSetup.manufacturer}${currentBrewSetup.model ? ` ${currentBrewSetup.model}` : ''}` : 'Brew'}
		>
			<img src={currentBrewSetup?.avatar ?? `/img/method-${currentBrewSetup?.method_type ?? 'espresso'}.png`} alt="" class="w-full h-full object-cover" />
		</button>
		{#if openPanel === 'brew'}
			<div class="absolute right-0 top-full mt-1">
				<SwitcherPopover
					items={brewItems}
					activeId={currentBrewSetupId}
					addLabel={$t('brewing.add')}
					onSelect={selectBrewSetup}
					onAdd={() => openAdd('brew')}
					onEdit={openEditBrewSetup}
				/>
			</div>
		{/if}
	</div>
</div>

{#if dialogState}
	<EditDialog
		dialog={dialogState}
		{brewMethodTypes}
		onSaved={onDialogSaved}
		onDeleted={onDialogDeleted}
		onClose={() => dialogState = null}
	/>
{/if}
