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

	async function toggleDefault() {
		await api.grinders.update(grinder.id, { is_default: !grinder.is_default });
		onUpdated();
	}

	async function toggleKind() {
		await api.grinders.update(grinder.id, { kind: grinder.kind === 'manual' ? 'auto' : 'manual' });
		onUpdated();
	}

	async function deleteGrinder() {
		if (!confirm(`Delete "${grinder.name}"?`)) return;
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
				{grinder.name}
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
				<p class="text-stone-700 font-medium text-lg">{grinder.name}</p>
				{#if grinder.model}
					<p class="text-sm text-stone-400">{grinder.model}</p>
				{/if}
			</div>
		</div>

		<div class="flex items-center gap-6 pt-2">
			<div class="flex items-center gap-3">
				<button onclick={toggleDefault}
					class="relative inline-flex h-6 w-12 items-center rounded-full transition-colors
						{grinder.is_default ? 'bg-amber-600' : 'bg-stone-300'}"
					title={$t('common.set_default')}
				>
					<span class="inline-block h-4 w-4 rounded-full bg-white shadow transition-transform
						{grinder.is_default ? 'translate-x-7' : 'translate-x-1'}"></span>
				</button>
				<span class="text-sm text-stone-500">{$t('common.default')}</span>
			</div>

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
	</div>
</div>
