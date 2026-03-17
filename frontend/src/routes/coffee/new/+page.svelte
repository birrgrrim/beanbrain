<script lang="ts">
	import { goto } from '$app/navigation';
	import { api, type Descriptor } from '$lib/api';
	import DescriptorPicker from '$lib/components/DescriptorPicker.svelte';

	let name = $state('');
	let roastery = $state('');
	let origin = $state('');
	let process = $state('');
	let roastLevel = $state('');
	let roasteryUrl = $state('');
	let notes = $state('');
	let selectedDescriptors = $state<number[]>([]);
	let descriptors = $state<Descriptor[]>([]);
	let saving = $state(false);

	$effect(() => {
		api.descriptors.list().then(d => descriptors = d);
	});

	function toggleDescriptor(id: number) {
		if (selectedDescriptors.includes(id)) {
			selectedDescriptors = selectedDescriptors.filter(d => d !== id);
		} else {
			selectedDescriptors = [...selectedDescriptors, id];
		}
	}

	async function handleSubmit(e: Event) {
		e.preventDefault();
		if (!name.trim() || !roastery.trim()) return;

		saving = true;
		const coffee = await api.coffees.create({
			name: name.trim(),
			roastery: roastery.trim(),
			origin: origin.trim() || undefined,
			process: process.trim() || undefined,
			roast_level: roastLevel.trim() || undefined,
			roastery_url: roasteryUrl.trim() || undefined,
			notes: notes.trim() || undefined,
			roastery_descriptor_ids: selectedDescriptors.length > 0 ? selectedDescriptors : undefined,
		});
		goto(`/coffee/${coffee.id}`);
	}
</script>

<div class="max-w-2xl mx-auto space-y-6">
	<div class="flex items-center gap-3">
		<a href="/" class="text-stone-400 hover:text-stone-600 transition-colors">&larr;</a>
		<h1 class="text-2xl font-bold text-stone-800">Add Coffee</h1>
	</div>

	<form onsubmit={handleSubmit} class="bg-white rounded-xl border border-stone-200 p-6 space-y-4">
		<div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
			<div>
				<label for="name" class="block text-sm font-medium text-stone-700 mb-1">Name *</label>
				<input
					id="name" type="text" bind:value={name} required
					class="w-full px-3 py-2 rounded-lg border border-stone-300 focus:outline-none focus:ring-2 focus:ring-amber-500"
					placeholder="Ethiopia Yirgacheffe"
				/>
			</div>
			<div>
				<label for="roastery" class="block text-sm font-medium text-stone-700 mb-1">Roastery *</label>
				<input
					id="roastery" type="text" bind:value={roastery} required
					class="w-full px-3 py-2 rounded-lg border border-stone-300 focus:outline-none focus:ring-2 focus:ring-amber-500"
					placeholder="Local Roasters"
				/>
			</div>
		</div>

		<div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
			<div>
				<label for="origin" class="block text-sm font-medium text-stone-700 mb-1">Origin</label>
				<input
					id="origin" type="text" bind:value={origin}
					class="w-full px-3 py-2 rounded-lg border border-stone-300 focus:outline-none focus:ring-2 focus:ring-amber-500"
					placeholder="Ethiopia"
				/>
			</div>
			<div>
				<label for="process" class="block text-sm font-medium text-stone-700 mb-1">Process</label>
				<input
					id="process" type="text" bind:value={process}
					class="w-full px-3 py-2 rounded-lg border border-stone-300 focus:outline-none focus:ring-2 focus:ring-amber-500"
					placeholder="Washed"
				/>
			</div>
			<div>
				<label for="roast_level" class="block text-sm font-medium text-stone-700 mb-1">Roast Level</label>
				<input
					id="roast_level" type="text" bind:value={roastLevel}
					class="w-full px-3 py-2 rounded-lg border border-stone-300 focus:outline-none focus:ring-2 focus:ring-amber-500"
					placeholder="Light"
				/>
			</div>
		</div>

		<div>
			<label for="url" class="block text-sm font-medium text-stone-700 mb-1">Roastery URL</label>
			<input
				id="url" type="url" bind:value={roasteryUrl}
				class="w-full px-3 py-2 rounded-lg border border-stone-300 focus:outline-none focus:ring-2 focus:ring-amber-500"
				placeholder="https://roastery.com/coffee"
			/>
		</div>

		<div>
			<label for="notes" class="block text-sm font-medium text-stone-700 mb-1">Notes</label>
			<textarea
				id="notes" bind:value={notes} rows={2}
				class="w-full px-3 py-2 rounded-lg border border-stone-300 focus:outline-none focus:ring-2 focus:ring-amber-500 resize-none"
				placeholder="Any notes about this coffee..."
			></textarea>
		</div>

		<div>
			<p class="text-sm font-medium text-stone-700 mb-2">Roastery Descriptors</p>
			<DescriptorPicker {descriptors} selected={selectedDescriptors} onToggle={toggleDescriptor} />
		</div>

		<div class="pt-2 flex gap-3">
			<button
				type="submit"
				disabled={saving || !name.trim() || !roastery.trim()}
				class="px-6 py-2.5 bg-amber-700 text-white rounded-lg hover:bg-amber-800 transition-colors
					font-medium disabled:opacity-50 disabled:cursor-not-allowed"
			>
				{saving ? 'Saving...' : 'Add Coffee'}
			</button>
			<a href="/" class="px-6 py-2.5 text-stone-600 hover:text-stone-800 transition-colors">Cancel</a>
		</div>
	</form>
</div>
