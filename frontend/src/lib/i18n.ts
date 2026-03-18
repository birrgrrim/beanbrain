import { derived } from 'svelte/store';
import { lang } from './lang';

const translations: Record<string, Record<string, string>> = {
	// Top bar & tabs
	'tab.coffee': { en: 'Coffee', uk: 'Кава' },
	'tab.grinding': { en: 'Grind', uk: 'Помол' },
	'tab.brewing': { en: 'Brew', uk: 'Заварювання' },
	'tab.roasteries': { en: 'Roast', uk: 'Ростерні' },

	// Coffee sidebar
	'sidebar.search': { en: 'Search coffees...', uk: 'Пошук кави...' },
	'sidebar.empty': { en: 'No coffees yet', uk: 'Кави ще немає' },
	'sidebar.no_matches': { en: 'No matches', uk: 'Нічого не знайдено' },

	// Empty state
	'empty.title': { en: 'Select a coffee', uk: 'Оберіть каву' },
	'empty.subtitle': { en: 'or add a new one to get started', uk: 'або додайте нову' },

	// Coffee detail
	'detail.origin': { en: 'Origin', uk: 'Країна' },
	'detail.process': { en: 'Process', uk: 'Обробка' },
	'detail.roast': { en: 'Roast', uk: 'Обсмаження' },
	'detail.score': { en: 'Score', uk: 'Оцінка' },
	'detail.sweet': { en: 'Sweet', uk: 'Солодкість' },
	'detail.acid': { en: 'Acid', uk: 'Кислотність' },
	'detail.bitter': { en: 'Bitter', uk: 'Гіркота' },
	'detail.flavor_profile': { en: 'Flavor profile', uk: 'Профіль смаку' },
	'detail.roastery_link': { en: 'View on roastery site', uk: 'Переглянути на сайті' },
	'detail.edit': { en: 'edit', uk: 'змінити' },
	'detail.delete': { en: 'Delete', uk: 'Видалити' },
	'detail.notes': { en: 'Roaster comment', uk: 'Коментар обсмажувача' },
	'detail.delete_confirm': { en: 'Delete this coffee and all its tastings?', uk: 'Видалити цю каву та всі дегустації?' },

	// Grinder settings (in coffee detail)
	'grinder.title': { en: 'Grinder Setting', uk: 'Налаштування помолу' },
	'grinder.add': { en: '+ Add', uk: '+ Додати' },
	'grinder.no_setting': { en: 'No setting recorded yet', uk: 'Ще немає налаштувань' },
	'grinder.setting': { en: 'Setting', uk: 'Помол' },
	'grinder.notes': { en: 'Notes', uk: 'Нотатки' },
	'grinder.save': { en: 'Save', uk: 'Зберегти' },
	'grinder.cancel': { en: 'Cancel', uk: 'Скасувати' },

	// Reviews
	'tasting.title': { en: 'Reviews', uk: 'Відгуки' },
	'tasting.add': { en: '+ Add Review', uk: '+ Додати відгук' },
	'tasting.empty': { en: 'No reviews yet', uk: 'Ще немає відгуків' },
	'tasting.who': { en: "Who's reviewing?", uk: 'Хто оцінює?' },
	'tasting.select': { en: 'Select person...', uk: 'Оберіть персону...' },
	'tasting.no_tasters': { en: 'Add a person via the switcher first', uk: 'Спочатку додайте персону' },
	'tasting.rating': { en: 'Rating', uk: 'Оцінка' },
	'tasting.comment': { en: 'Comment', uk: 'Коментар' },
	'tasting.comment_placeholder': { en: 'What did you taste?', uk: 'Що ви відчули?' },
	'tasting.flavors': { en: 'Flavors you taste', uk: 'Смаки які ви відчуваєте' },
	'tasting.save': { en: 'Save Review', uk: 'Зберегти відгук' },
	'tasting.cancel': { en: 'Cancel', uk: 'Скасувати' },

	// Add coffee
	'add.title': { en: 'Add Coffee', uk: 'Додати каву' },
	'add.url_hint': { en: 'Paste a roastery URL to auto-fill', uk: 'Вставте посилання для автозаповнення' },
	'add.fetch': { en: 'Fetch', uk: 'Завантажити' },
	'add.fetching': { en: 'Fetching...', uk: 'Завантаження...' },
	'add.name': { en: 'Name', uk: 'Назва' },
	'add.roastery': { en: 'Roastery', uk: 'Обсмажувач' },
	'add.origin': { en: 'Origin', uk: 'Країна' },
	'add.process': { en: 'Process', uk: 'Обробка' },
	'add.roast_level': { en: 'Roast Level', uk: 'Рівень обсмаження' },
	'add.notes': { en: 'Notes', uk: 'Нотатки' },
	'add.descriptors': { en: 'Roastery Descriptors', uk: 'Дескриптори обсмажувача' },
	'add.save': { en: 'Add Coffee', uk: 'Додати каву' },
	'add.saving': { en: 'Saving...', uk: 'Збереження...' },
	'add.cancel': { en: 'Cancel', uk: 'Скасувати' },

	// Descriptor autocomplete
	'desc.search': { en: 'Search flavors...', uk: 'Пошук смаків...' },
	'desc.suggested': { en: 'Roastery suggests', uk: 'Обсмажувач рекомендує' },

	// Person switcher
	'person.everyone': { en: 'Everyone', uk: 'Усі' },
	'person.add_new': { en: 'Add person...', uk: 'Додати персону...' },
	'persons.add_placeholder': { en: 'Name...', uk: "Ім'я..." },
	'persons.add': { en: 'Add', uk: 'Додати' },

	// Grinding tab (sidebar + detail)
	'grinding.title': { en: 'Grinders', uk: 'Кавомолки' },
	'grinding.empty': { en: 'No grinders yet', uk: 'Кавомолок ще немає' },
	'grinding.search': { en: 'Search grinders...', uk: 'Пошук кавомолок...' },
	'grinding.empty_hint': { en: 'Add your first grinder', uk: 'Додайте першу кавомолку' },
	'grinding.add': { en: 'Add Grinder', uk: 'Додати кавомолку' },
	'grinding.name': { en: 'Name', uk: 'Назва' },
	'grinding.name_placeholder': { en: 'e.g. Eureka Mignon', uk: 'напр. Eureka Mignon' },
	'grinding.model': { en: 'Model', uk: 'Модель' },
	'grinding.model_placeholder': { en: 'Model (optional)', uk: 'Модель (необов.)' },
	'grinding.select': { en: 'Select a grinder', uk: 'Оберіть кавомолку' },

	// Brewing tab (sidebar + detail)
	'brewing.title': { en: 'Brew Setups', uk: 'Налаштування заварювання' },
	'brewing.empty': { en: 'No brew setups yet', uk: 'Налаштувань ще немає' },
	'brewing.search': { en: 'Search setups...', uk: 'Пошук налаштувань...' },
	'brewing.empty_hint': { en: 'Add your first brew setup', uk: 'Додайте перше налаштування' },
	'brewing.add': { en: 'Add Setup', uk: 'Додати' },
	'brewing.pick_method': { en: 'Choose brew method', uk: 'Оберіть метод' },
	'brewing.name': { en: 'Name', uk: 'Назва' },
	'brewing.name_placeholder': { en: 'e.g. Gaggia Classic', uk: 'напр. Gaggia Classic' },
	'brewing.basket': { en: 'Basket size (g)', uk: 'Розмір кошика (г)' },
	'brewing.select': { en: 'Select a brew setup', uk: 'Оберіть налаштування' },

	// Brew method type names
	'method.espresso': { en: 'Espresso', uk: 'Еспресо' },
	'method.pourover': { en: 'Pour Over', uk: 'Пуровер' },
	'method.aeropress': { en: 'AeroPress', uk: 'Аеропрес' },
	'method.frenchpress': { en: 'French Press', uk: 'Френч-прес' },
	'method.moka': { en: 'Moka Pot', uk: 'Мока' },
	'method.cezve': { en: 'Cezve', uk: 'Джезва' },

	// Roasteries tab
	'roastery.title': { en: 'Roasteries', uk: 'Обсмажувачі' },
	'roastery.add': { en: 'Add Roastery', uk: 'Додайте ростерню' },
	'roastery.name': { en: 'Name', uk: 'Назва' },
	'roastery.website': { en: 'Website', uk: 'Веб-сайт' },
	'roastery.search': { en: 'Search roasteries...', uk: 'Пошук обсмажувачів...' },
	'roastery.empty': { en: 'No roasteries yet', uk: 'Обсмажувачів ще немає' },
	'roastery.select': { en: 'Select a roastery', uk: 'Оберіть ростерню' },

	// Common
	'common.optional': { en: 'Optional', uk: 'Необов\'язково' },
	'common.default': { en: 'default', uk: 'за замовч.' },
	'common.set_default': { en: 'set default', uk: 'за замовч.' },
	'common.save': { en: 'Save', uk: 'Зберегти' },
	'common.cancel': { en: 'Cancel', uk: 'Скасувати' },
};

export const t = derived(lang, ($lang) => {
	return (key: string): string => {
		const entry = translations[key];
		if (!entry) return key;
		return entry[$lang] || entry['en'] || key;
	};
});
