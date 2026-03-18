<script lang="ts">
	import { api, type Roastery } from '$lib/api';
	import { t } from '$lib/i18n';
	import Icons from './Icons.svelte';

	let { roastery, onUpdated, onDeleted, onBack }: {
		roastery: Roastery;
		onUpdated: () => void;
		onDeleted: () => void;
		onBack: () => void;
	} = $props();

	async function deleteRoastery() {
		if (!confirm(`Delete "${roastery.name}"?`)) return;
		await api.roasteries.delete(roastery.id);
		onDeleted();
	}
</script>

<div class="max-w-2xl mx-auto p-10 space-y-8">
	<div class="flex items-start justify-between">
		<div class="flex items-center gap-3">
			<button onclick={onBack}
				class="p-1.5 text-stone-400 hover:text-stone-600 transition-colors rounded-lg hover:bg-card-inset"
				title="Back">
				<Icons icon="back" size={18} />
			</button>
			<img src="/img/roastery.png" alt="" class="w-8 h-8 opacity-70" />
			<h2 class="text-3xl font-bold text-stone-800" style="font-family: 'DM Serif Display', serif;">
				{roastery.name}
			</h2>
		</div>
		<button onclick={deleteRoastery}
			class="p-2 text-stone-400 hover:text-red-500 transition-colors rounded hover:bg-card-inset"
			title={$t('detail.delete')}>
			<img src="/img/knockbox.png" alt="delete" class="w-7 h-7 opacity-50" />
		</button>
	</div>

	<div class="bg-card rounded-2xl border border-stone-100 shadow-sm animate-card p-6 space-y-4">
		<div class="flex items-center gap-4">
			<img src="/img/roastery.png" alt="" class="w-16 h-16 opacity-60" />
			<div class="space-y-1">
				<p class="text-stone-700 font-medium text-lg">{roastery.name}</p>
				{#if roastery.website}
					<a href={roastery.website} target="_blank" rel="noopener"
						class="inline-flex items-center gap-1.5 text-sm text-amber-600 hover:text-amber-800">
						<Icons icon="link" size={12} /> {roastery.website}
					</a>
				{/if}
			</div>
		</div>
	</div>
</div>
