<script lang="ts">
	import type { Grinder } from '$lib/api';
	import { t } from '$lib/i18n';
	import Icons from './Icons.svelte';

	let { grinders = [], selectedId = null, onSelect, onAdd }: {
		grinders: Grinder[];
		selectedId: number | null;
		onSelect: (id: number) => void;
		onAdd: () => void;
	} = $props();

	let search = $state('');
	let filtered = $derived(
		search.trim()
			? grinders.filter(g =>
				g.name.toLowerCase().includes(search.toLowerCase()) ||
				(g.model?.toLowerCase().includes(search.toLowerCase()) ?? false)
			)
			: grinders
	);
</script>

<aside class="w-[420px] flex-shrink-0 bg-card border-r border-stone-200 flex flex-col">
	<div class="p-4 border-b border-stone-100">
		<div class="flex items-center gap-2">
			<div class="relative flex-1">
				<Icons icon="search" size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-stone-300" />
				<input
					type="text"
					bind:value={search}
					placeholder={$t('grinding.search')}
					class="w-full pl-9 pr-4 py-2.5 rounded-lg border border-stone-200 bg-card-inset text-base
						focus:outline-none focus:ring-2 focus:ring-amber-400/50 focus:border-amber-300
						placeholder:text-stone-400"
				/>
			</div>
			<button
				onclick={onAdd}
				class="w-10 h-10 flex items-center justify-center rounded-lg flex-shrink-0
					bg-amber-700 text-white hover:bg-amber-800 transition-colors"
				title={$t('grinding.add')}
			>
				<Icons icon="plus" size={20} />
			</button>
		</div>
	</div>

	<div class="flex-1 overflow-y-auto">
		{#if grinders.length === 0}
			<div class="p-6 text-center">
				<img src="/img/select-grinder.png" alt="" class="mx-auto mb-3 opacity-60" style="max-width: 140px;" />
				<p class="text-sm text-stone-500">{$t('grinding.empty')}</p>
				<p class="text-xs text-stone-400 mt-1">{$t('grinding.empty_hint')}</p>
			</div>
		{:else if filtered.length === 0}
			<div class="p-6 text-center">
				<p class="text-sm text-stone-500">{$t('sidebar.no_matches')}</p>
			</div>
		{:else}
			{#each filtered as grinder}
				<button
					onclick={() => onSelect(grinder.id)}
					class="w-full text-left px-5 py-4 border-b border-stone-50 transition-colors
						hover:bg-amber-50/50
						{selectedId === grinder.id ? 'bg-amber-50 border-l-2 border-l-amber-600' : ''}"
				>
					<div class="flex items-center gap-3">
						<img src="/img/grinder-{grinder.kind === 'manual' ? 'manual' : 'auto'}.png" alt="" class="w-10 h-10 opacity-60" />
						<div class="min-w-0 flex-1">
							<p class="font-semibold text-lg text-stone-800 truncate">{grinder.name}</p>
							<div class="flex items-center gap-2 mt-0.5">
								{#if grinder.model}
									<span class="text-sm text-stone-400 truncate">{grinder.model}</span>
								{/if}
								{#if grinder.is_default}
									<span class="text-xs bg-amber-100 text-amber-700 rounded-md px-2 py-0.5">{$t('common.default')}</span>
								{/if}
							</div>
						</div>
					</div>
				</button>
			{/each}
		{/if}
	</div>
</aside>
