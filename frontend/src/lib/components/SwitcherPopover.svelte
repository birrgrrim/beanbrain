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
		addLabel,
		onSelect,
		onAdd,
		onEdit,
	}: {
		items: Item[];
		activeId: number | null;
		everyoneLabel?: string;
		addLabel: string;
		onSelect: (id: number | null) => void;
		onAdd: () => void;
		onEdit?: (id: number) => void;
	} = $props();
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
					{#if onEdit}
						<button
							onclick={(e) => { e.stopPropagation(); onEdit(item.id); }}
							class="p-2 mr-1 text-stone-300 hover:text-amber-600 transition-colors rounded flex-shrink-0"
							title="Edit"
						>
							<Icons icon="edit" size={14} />
						</button>
					{/if}
				</div>
			{/each}
		</div>
	{/if}

	<div class="border-t border-stone-100">
		<button
			onclick={(e) => { e.stopPropagation(); onAdd(); }}
			class="w-full text-left px-4 py-3 text-sm text-amber-600 hover:bg-amber-50/50 transition-colors flex items-center gap-3"
		>
			<Icons icon="plus" size={14} />
			{addLabel}
		</button>
	</div>
</div>
