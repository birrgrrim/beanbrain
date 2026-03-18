<script lang="ts">
	import { api, type Taster } from '$lib/api';
	import { t } from '$lib/i18n';
	import { activePerson } from '$lib/personStore';
	import Icons from './Icons.svelte';

	let { onChange }: { onChange: () => void } = $props();

	let tasters = $state<Taster[]>([]);
	let open = $state(false);
	let adding = $state(false);
	let newName = $state('');
	let currentPersonId = $state<number | null>(null);

	activePerson.subscribe(v => currentPersonId = v);

	async function load() {
		tasters = await api.tasters.list();
		// If stored person no longer exists, clear it
		if (currentPersonId !== null && !tasters.some(t => t.id === currentPersonId)) {
			activePerson.set(null);
		}
	}

	$effect(() => { load(); });

	function selectPerson(id: number | null) {
		activePerson.set(id);
		open = false;
		onChange();
	}

	async function addPerson() {
		if (!newName.trim()) return;
		const created = await api.tasters.create(newName.trim());
		newName = '';
		adding = false;
		await load();
		selectPerson(created.id);
	}

	async function removePerson(id: number) {
		await api.tasters.delete(id);
		if (currentPersonId === id) {
			activePerson.set(null);
		}
		await load();
		onChange();
	}

	const currentPerson = $derived(tasters.find(t => t.id === currentPersonId));

	function handleClickOutside(event: MouseEvent) {
		const target = event.target as HTMLElement;
		if (!target.closest('.person-switcher')) {
			open = false;
			adding = false;
		}
	}
</script>

<svelte:window onclick={handleClickOutside} />

<div class="person-switcher relative">
	<button
		onclick={() => open = !open}
		class="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium
			bg-card-inset hover:bg-parchment transition-colors text-stone-500"
	>
		<img src="/img/tab-person.png" alt="" class="w-6 h-6 {currentPerson ? 'opacity-80' : 'opacity-40'}" />
		<span class="max-w-[120px] truncate">{currentPerson ? currentPerson.name : $t('person.everyone')}</span>
		<Icons icon="chevron" size={12} className="text-stone-400" />
	</button>

	{#if open}
		<div class="absolute right-0 top-full mt-1 w-72 bg-card rounded-xl border border-stone-200 shadow-lg z-50 overflow-hidden">
			<!-- "Everyone" option (average) -->
			<button
				onclick={() => selectPerson(null)}
				class="w-full text-left px-4 py-3 text-sm hover:bg-amber-50/50 transition-colors flex items-center gap-3
					{currentPersonId === null ? 'bg-amber-50 text-amber-700 font-medium' : 'text-stone-600'}"
			>
				<span class="w-6 h-6 rounded-full bg-stone-100 flex items-center justify-center text-xs text-stone-400">
					<Icons icon="users" size={14} />
				</span>
				{$t('person.everyone')}
			</button>

			{#if tasters.length > 0}
				<div class="border-t border-stone-100">
					{#each tasters as taster}
						<div class="flex items-center hover:bg-amber-50/50 transition-colors
							{currentPersonId === taster.id ? 'bg-amber-50' : ''}">
							<button
								onclick={() => selectPerson(taster.id)}
								class="flex-1 text-left px-4 py-3 text-sm flex items-center gap-3
									{currentPersonId === taster.id ? 'text-amber-700 font-medium' : 'text-stone-600'}"
							>
								<img src="/img/tab-person.png" alt="" class="w-6 h-6 opacity-60" />
								{taster.name}
							</button>
							<button
								onclick={(e) => { e.stopPropagation(); removePerson(taster.id); }}
								class="p-2 mr-2 text-stone-300 hover:text-red-400 transition-colors rounded"
								title={$t('detail.delete')}
							>
								<img src="/img/knockbox.png" alt="delete" class="w-5 h-5 opacity-50" />
							</button>
						</div>
					{/each}
				</div>
			{/if}

			<!-- Add new person -->
			<div class="border-t border-stone-100">
				{#if adding}
					<div class="p-3 flex gap-2">
						<input
							type="text"
							bind:value={newName}
							placeholder={$t('persons.add_placeholder')}
							class="flex-1 px-3 py-2 rounded-lg border border-stone-200 text-sm bg-card
								focus:outline-none focus:ring-2 focus:ring-amber-400/50"
							onkeydown={(e) => { if (e.key === 'Enter') { e.preventDefault(); addPerson(); } if (e.key === 'Escape') { adding = false; newName = ''; } }}
						/>
						<button
							onclick={addPerson}
							disabled={!newName.trim()}
							class="px-3 py-2 bg-amber-700 text-white rounded-lg text-sm hover:bg-amber-800
								transition-colors disabled:opacity-50"
						>{$t('persons.add')}</button>
					</div>
				{:else}
					<button
						onclick={(e) => { e.stopPropagation(); adding = true; }}
						class="w-full text-left px-4 py-3 text-sm text-amber-600 hover:bg-amber-50/50 transition-colors flex items-center gap-3"
					>
						<Icons icon="plus" size={14} />
						{$t('person.add_new')}
					</button>
				{/if}
			</div>
		</div>
	{/if}
</div>
