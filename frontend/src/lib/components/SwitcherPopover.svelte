<script lang="ts">
	import { t } from '$lib/i18n';
	import Icons from './Icons.svelte';

	interface Item {
		id: number;
		label: string;
		sublabel?: string;
		icon?: string;
	}

	let {
		items,
		activeId,
		everyoneLabel = '',
		addPlaceholder,
		addLabel,
		onSelect,
		onAdd,
		onRemove,
	}: {
		items: Item[];
		activeId: number | null;
		everyoneLabel?: string;
		addPlaceholder: string;
		addLabel: string;
		onSelect: (id: number | null) => void;
		onAdd: (name: string) => void;
		onRemove?: (id: number) => void;
	} = $props();

	let adding = $state(false);
	let newName = $state('');

	function handleAdd() {
		if (!newName.trim()) return;
		onAdd(newName.trim());
		newName = '';
		adding = false;
	}
</script>

<div class="w-72 bg-card rounded-xl border border-stone-200 shadow-lg z-50 overflow-hidden">
	{#if everyoneLabel}
		<button
			onclick={() => onSelect(null)}
			class="w-full text-left px-4 py-3 text-sm hover:bg-amber-50/50 transition-colors flex items-center gap-3
				{activeId === null ? 'bg-amber-50 text-amber-700 font-medium' : 'text-stone-600'}"
		>
			<span class="w-6 h-6 rounded-full bg-stone-100 flex items-center justify-center text-xs text-stone-400">
				<Icons icon="users" size={14} />
			</span>
			{everyoneLabel}
		</button>
	{/if}

	{#if items.length > 0}
		<div class="border-t border-stone-100">
			{#each items as item}
				<div class="flex items-center hover:bg-amber-50/50 transition-colors
					{activeId === item.id ? 'bg-amber-50' : ''}">
					<button
						onclick={() => onSelect(item.id)}
						class="flex-1 text-left px-4 py-3 text-sm flex items-center gap-3 min-w-0
							{activeId === item.id ? 'text-amber-700 font-medium' : 'text-stone-600'}"
					>
						{#if item.icon}
							<img src={item.icon} alt="" class="w-6 h-6 opacity-60 flex-shrink-0" />
						{/if}
						<div class="min-w-0 flex-1">
							<span class="truncate block">{item.label}</span>
							{#if item.sublabel}
								<span class="text-xs text-stone-400 truncate block">{item.sublabel}</span>
							{/if}
						</div>
					</button>
					{#if onRemove}
						<button
							onclick={(e) => { e.stopPropagation(); onRemove(item.id); }}
							class="p-2 mr-2 text-stone-300 hover:text-red-400 transition-colors rounded flex-shrink-0"
							title={$t('detail.delete')}
						>
							<img src="/img/knockbox.png" alt="delete" class="w-5 h-5 opacity-50" />
						</button>
					{/if}
				</div>
			{/each}
		</div>
	{/if}

	<div class="border-t border-stone-100">
		{#if adding}
			<div class="p-3 flex gap-2">
				<input
					type="text"
					bind:value={newName}
					placeholder={addPlaceholder}
					class="flex-1 px-3 py-2 rounded-lg border border-stone-200 text-sm bg-card
						focus:outline-none focus:ring-2 focus:ring-amber-400/50"
					onkeydown={(e) => { if (e.key === 'Enter') { e.preventDefault(); handleAdd(); } if (e.key === 'Escape') { adding = false; newName = ''; } }}
				/>
				<button
					onclick={handleAdd}
					disabled={!newName.trim()}
					class="px-3 py-2 bg-amber-700 text-white rounded-lg text-sm hover:bg-amber-800
						transition-colors disabled:opacity-50"
				>{addLabel}</button>
			</div>
		{:else}
			<button
				onclick={(e) => { e.stopPropagation(); adding = true; }}
				class="w-full text-left px-4 py-3 text-sm text-amber-600 hover:bg-amber-50/50 transition-colors flex items-center gap-3"
			>
				<Icons icon="plus" size={14} />
				{addLabel}
			</button>
		{/if}
	</div>
</div>
