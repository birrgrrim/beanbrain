import { api, type Origin, type Roastery, type Descriptor, type Taster, type Grinder, type BrewSetup } from './api';

let _origins: Origin[] | null = null;
let _roasteries: Roastery[] | null = null;
let _descriptors: Descriptor[] | null = null;
let _tasters: Taster[] | null = null;
let _grinders: Grinder[] | null = null;
let _brewSetups: BrewSetup[] | null = null;

export const refData = {
	origins: async () => { if (!_origins) _origins = await api.origins.list(); return _origins; },
	roasteries: async () => { if (!_roasteries) _roasteries = await api.roasteries.list(); return _roasteries; },
	descriptors: async () => { if (!_descriptors) _descriptors = await api.descriptors.list(); return _descriptors; },
	tasters: async () => { if (!_tasters) _tasters = await api.tasters.list(); return _tasters; },
	grinders: async () => { if (!_grinders) _grinders = await api.grinders.list(); return _grinders; },
	brewSetups: async () => { if (!_brewSetups) _brewSetups = await api.brewSetups.list(); return _brewSetups; },
	invalidate: (key?: 'origins' | 'roasteries' | 'descriptors' | 'tasters' | 'grinders' | 'brewSetups') => {
		if (key) {
			if (key === 'origins') _origins = null;
			else if (key === 'roasteries') _roasteries = null;
			else if (key === 'descriptors') _descriptors = null;
			else if (key === 'tasters') _tasters = null;
			else if (key === 'grinders') _grinders = null;
			else if (key === 'brewSetups') _brewSetups = null;
		} else {
			_origins = _roasteries = _descriptors = _tasters = _grinders = _brewSetups = null;
		}
	},
};
