<script lang="ts">
	import { api, type Grinder } from '$lib/api';
	import { t } from '$lib/i18n';
	import Icons from './Icons.svelte';

	let { grinder, onUpdated, onDeleted, onBack }: {
		grinder: Grinder;
		onUpdated: () => void;
		onDeleted: () => void;
		onBack: () => void;
	} = $props();


	async function toggleKind() {
		await api.grinders.update(grinder.id, { kind: grinder.kind === 'manual' ? 'auto' : 'manual' });
		onUpdated();
	}

	let editRangeMin = $state(0);
	let editRangeMax = $state<number | string>('');
	let editStep = $state(1);
	$effect(() => {
		editRangeMin = grinder.range_min;
		editRangeMax = grinder.range_max ?? '';
		editStep = grinder.step;
	});

	async function saveRange() {
		await api.grinders.update(grinder.id, {
			range_min: Number(editRangeMin) || 0,
			range_max: editRangeMax !== '' ? Number(editRangeMax) : null,
			step: Number(editStep) || 1,
		});
		onUpdated();
	}

	async function deleteGrinder() {
		if (!confirm(`Delete "${grinder.manufacturer}"?`)) return;
		await api.grinders.delete(grinder.id);
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
			<img src="/img/grinder-{grinder.kind === 'manual' ? 'manual' : 'auto'}.png" alt="" class="w-8 h-8 opacity-70" />
			<h2 class="text-3xl font-bold text-stone-800" style="font-family: 'DM Serif Display', serif;">
				{grinder.manufacturer}
			</h2>
		</div>
		<button onclick={deleteGrinder}
			class="p-2 text-stone-400 hover:text-red-500 transition-colors rounded hover:bg-card-inset"
			title={$t('detail.delete')}>
			<img src="/img/knockbox.png" alt="delete" class="w-7 h-7 opacity-50" />
		</button>
	</div>

	<div class="bg-card rounded-2xl border border-stone-100 shadow-sm animate-card p-6 space-y-4">
		<div class="flex items-center gap-4">
			<img src="/img/grinder-{grinder.kind === 'manual' ? 'manual' : 'auto'}.png" alt="" class="w-16 h-16 opacity-60" />
			<div class="space-y-1">
				<p class="text-stone-700 font-medium text-lg">{grinder.manufacturer}</p>
				{#if grinder.model}
					<p class="text-sm text-stone-400">{grinder.model}</p>
				{/if}
			</div>
		</div>

		<div class="flex items-center gap-6 pt-2">
			<div class="flex items-center gap-3">
				<button onclick={toggleKind}
					class="relative inline-flex h-6 w-12 items-center rounded-full transition-colors
						{grinder.kind === 'manual' ? 'bg-amber-600' : 'bg-stone-300'}"
					title="Toggle manual/auto"
				>
					<span class="inline-block h-4 w-4 rounded-full bg-white shadow transition-transform
						{grinder.kind === 'manual' ? 'translate-x-7' : 'translate-x-1'}"></span>
				</button>
				<span class="text-sm text-stone-500">{grinder.kind === 'manual' ? 'Manual' : 'Auto'}</span>
			</div>
		</div>

		<div class="border-t border-stone-100 pt-4">
			<label class="text-xs text-stone-400 uppercase tracking-wide">{$t('grinding.range')}</label>
			<div class="flex items-center gap-2 mt-2">
				<input type="number" bind:value={editRangeMin} placeholder="0"
					class="w-24 px-3 py-2 rounded-lg border border-stone-200 text-base bg-card-inset text-center
						focus:outline-none focus:ring-2 focus:ring-amber-400/50" />
				<span class="text-stone-400">—</span>
				<input type="number" bind:value={editRangeMax} placeholder="∞"
					class="w-24 px-3 py-2 rounded-lg border border-stone-200 text-base bg-card-inset text-center
						focus:outline-none focus:ring-2 focus:ring-amber-400/50" />
				<span class="text-xs text-stone-400 mx-1">{$t('grinding.step')}</span>
				<input type="number" bind:value={editStep} placeholder="1" min="0.1" step="0.1"
					class="w-20 px-3 py-2 rounded-lg border border-stone-200 text-base bg-card-inset text-center
						focus:outline-none focus:ring-2 focus:ring-amber-400/50" />
				<button onclick={saveRange}
					class="ml-2 px-4 py-2 bg-amber-700 text-white rounded-lg text-sm hover:bg-amber-800">
					{$t('common.save')}
				</button>
			</div>
		</div>
	</div>
</div>
