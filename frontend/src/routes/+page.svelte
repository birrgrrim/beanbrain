<script lang="ts">
	import { api, type CoffeeListItem } from '$lib/api';

	let coffees = $state<CoffeeListItem[]>([]);
	let search = $state('');
	let loading = $state(true);

	async function loadCoffees() {
		loading = true;
		coffees = await api.coffees.list(search || undefined);
		loading = false;
	}

	$effect(() => {
		loadCoffees();
	});

	let debounceTimer: ReturnType<typeof setTimeout>;
	function handleSearch(e: Event) {
		const value = (e.target as HTMLInputElement).value;
		search = value;
		clearTimeout(debounceTimer);
		debounceTimer = setTimeout(() => loadCoffees(), 300);
	}
</script>

<div class="space-y-6">
	<div class="flex items-center justify-between gap-4">
		<h1 class="text-2xl font-bold text-stone-800">Your Coffees</h1>
		<a
			href="/coffee/new"
			class="px-4 py-2 bg-amber-700 text-white rounded-lg hover:bg-amber-800 transition-colors font-medium text-sm"
		>
			+ Add Coffee
		</a>
	</div>

	<input
		type="text"
		placeholder="Search by name or roastery..."
		value={search}
		oninput={handleSearch}
		class="w-full px-4 py-2.5 rounded-lg border border-stone-300 bg-white
			focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent
			placeholder:text-stone-400"
	/>

	{#if loading}
		<div class="text-center py-12 text-stone-400">Loading...</div>
	{:else if coffees.length === 0}
		<div class="text-center py-12">
			<p class="text-stone-400 text-lg">No coffees yet</p>
			<p class="text-stone-400 text-sm mt-1">Add your first coffee to get started</p>
		</div>
	{:else}
		<div class="grid gap-3">
			{#each coffees as coffee}
				<a
					href="/coffee/{coffee.id}"
					class="block bg-white rounded-xl border border-stone-200 p-4 hover:shadow-md hover:border-amber-300 transition-all"
				>
					<div class="flex items-start gap-3">
						{#if coffee.image_url}
							<img src={coffee.image_url} alt={coffee.name} class="w-12 h-12 rounded-lg object-contain flex-shrink-0" />
						{/if}
						<div class="min-w-0">
							<h2 class="font-semibold text-stone-800 truncate">{coffee.name}</h2>
							<p class="text-sm text-stone-500">{coffee.roastery}</p>
							<div class="flex items-center gap-3 mt-1 text-xs text-stone-400">
								{#if coffee.origin}
									<span>{coffee.origin}</span>
								{/if}
								{#if coffee.roast_level}
									<span>{coffee.roast_level}</span>
								{/if}
							</div>
						</div>
					</div>

					{#if coffee.roastery_descriptors.length > 0}
						<div class="flex flex-wrap gap-1 mt-2">
							{#each coffee.roastery_descriptors as desc}
								<span class="px-2 py-0.5 rounded-full text-xs bg-amber-50 text-amber-700 border border-amber-200">
									{desc.name}
								</span>
							{/each}
						</div>
					{/if}
				</a>
			{/each}
		</div>
	{/if}
</div>
