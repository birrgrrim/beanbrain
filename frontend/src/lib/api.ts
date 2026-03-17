const BASE_URL = 'http://localhost:8000';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
	const res = await fetch(`${BASE_URL}${path}`, {
		headers: { 'Content-Type': 'application/json' },
		...options,
	});
	if (!res.ok) {
		throw new Error(`API error: ${res.status} ${res.statusText}`);
	}
	if (res.status === 204) return undefined as T;
	return res.json();
}

export interface Descriptor {
	id: number;
	name: string;
	category: string;
}

export interface Taster {
	id: number;
	name: string;
}

export interface Equipment {
	id: number;
	type: string;
	name: string;
	model: string | null;
	is_active: boolean;
}

export interface BrewMethod {
	id: number;
	name: string;
}

export interface BasketSize {
	id: number;
	size_grams: number;
	label: string;
}

export interface GrinderSetting {
	id: number;
	coffee_id: number;
	equipment_id: number;
	brew_method_id: number;
	basket_size_id: number | null;
	setting: number;
	notes: string | null;
	equipment: Equipment;
	brew_method: BrewMethod;
	basket_size: BasketSize | null;
}

export interface Tasting {
	id: number;
	coffee_id: number;
	taster_id: number;
	taster: Taster;
	rating: number;
	comment: string | null;
	tasted_at: string;
	descriptors: Descriptor[];
}

export interface Coffee {
	id: number;
	name: string;
	roastery: string;
	origin: string | null;
	process: string | null;
	roast_level: string | null;
	roastery_url: string | null;
	image_url: string | null;
	score: number | null;
	sweetness: string | null;
	acidity: string | null;
	bitterness: string | null;
	notes: string | null;
	created_at: string;
	roastery_descriptors: Descriptor[];
	tastings: Tasting[];
	grinder_settings: GrinderSetting[];
}

export interface CoffeeListItem {
	id: number;
	name: string;
	roastery: string;
	origin: string | null;
	roast_level: string | null;
	image_url: string | null;
	created_at: string;
	roastery_descriptors: Descriptor[];
}

export interface ScrapeResult {
	name: string;
	roastery: string;
	origin: string | null;
	process: string | null;
	roast_level: string | null;
	roastery_url: string;
	image_url: string | null;
	score: number | null;
	sweetness: string | null;
	acidity: string | null;
	bitterness: string | null;
	flavor_descriptors: Record<string, string[]>;
	name_i18n: Record<string, string>;
}

export const api = {
	coffees: {
		list: (search?: string) =>
			request<CoffeeListItem[]>(`/coffees/${search ? `?search=${encodeURIComponent(search)}` : ''}`),
		get: (id: number) => request<Coffee>(`/coffees/${id}`),
		create: (data: {
			name: string;
			roastery: string;
			origin?: string;
			process?: string;
			roast_level?: string;
			roastery_url?: string;
			image_url?: string;
			score?: number;
			sweetness?: string;
			acidity?: string;
			bitterness?: string;
			notes?: string;
			roastery_descriptor_ids?: number[];
		}) => request<Coffee>('/coffees/', { method: 'POST', body: JSON.stringify(data) }),
		update: (id: number, data: Record<string, unknown>) =>
			request<Coffee>(`/coffees/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
		delete: (id: number) => request<void>(`/coffees/${id}`, { method: 'DELETE' }),
	},
	tastings: {
		create: (coffeeId: number, data: {
			taster_id: number;
			rating: number;
			comment?: string;
			descriptor_ids?: number[];
		}) => request<Tasting>(`/coffees/${coffeeId}/tastings/`, {
			method: 'POST', body: JSON.stringify(data),
		}),
		delete: (coffeeId: number, tastingId: number) =>
			request<void>(`/coffees/${coffeeId}/tastings/${tastingId}`, { method: 'DELETE' }),
	},
	grinderSettings: {
		create: (coffeeId: number, data: {
			equipment_id: number;
			brew_method_id: number;
			basket_size_id?: number;
			setting: number;
			notes?: string;
		}) => request<GrinderSetting>(`/coffees/${coffeeId}/settings/`, {
			method: 'POST', body: JSON.stringify(data),
		}),
		delete: (coffeeId: number, settingId: number) =>
			request<void>(`/coffees/${coffeeId}/settings/${settingId}`, { method: 'DELETE' }),
	},
	tasters: {
		list: () => request<Taster[]>('/tasters/'),
		create: (name: string) => request<Taster>('/tasters/', {
			method: 'POST', body: JSON.stringify({ name }),
		}),
		delete: (id: number) => request<void>(`/tasters/${id}`, { method: 'DELETE' }),
	},
	descriptors: {
		list: () => request<Descriptor[]>('/descriptors/'),
	},
	equipment: {
		list: () => request<Equipment[]>('/equipment'),
		brewMethods: () => request<BrewMethod[]>('/brew-methods'),
		basketSizes: () => request<BasketSize[]>('/basket-sizes'),
	},
	scrape: (url: string) =>
		request<ScrapeResult>(`/scrape/?url=${encodeURIComponent(url)}`),
};
