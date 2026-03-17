<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';
	import '../app.css';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<title>BeanBrain</title>
</svelte:head>

<div class="min-h-screen bg-stone-50 text-stone-900">
	<nav class="bg-amber-900 text-amber-50 shadow-lg">
		<div class="max-w-5xl mx-auto px-4 py-3 flex items-center gap-3">
			<a href="/" class="text-xl font-bold tracking-tight hover:text-amber-200 transition-colors">
				BeanBrain
			</a>
			<span class="text-amber-300 text-sm">coffee tracker</span>
		</div>
	</nav>

	<main class="max-w-5xl mx-auto px-4 py-6">
		{@render children()}
	</main>
</div>
