<script lang="ts">
	interface Props {
		value: number;
		step?: number;
		class?: string;
	}

	let { value, step = 1, class: className = '' }: Props = $props();

	const isWholeStep = $derived(step % 1 === 0);
	const intPart = $derived(Math.floor(value));
	const decPart = $derived(isWholeStep ? '' : '.' + (value % 1 === 0 ? '0' : String(Math.round((value % 1) * 10))));
</script>

<span class="tabular-nums font-bold {className}">
	{intPart}{#if decPart}<span class="text-[0.6em] opacity-70">{decPart}</span>{/if}
</span>
