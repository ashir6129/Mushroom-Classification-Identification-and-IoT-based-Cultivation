-- ============================================================
-- Mushrooms Database
-- Total Records: 215
-- Created for Flutter SQLite Application
-- ============================================================

CREATE TABLE IF NOT EXISTS mushrooms (
    id              INTEGER PRIMARY KEY,
    sub_class       TEXT NOT NULL,
    scientific_name TEXT,
    kingdom         TEXT,
    family          TEXT,
    edibility       TEXT,
    description     TEXT,
    occurrence      TEXT,
    price_pkr       TEXT,
    recipes         TEXT
);

-- ============================================================
-- EDIBLE / NON-POISONOUS (104 records)
-- ============================================================

-- 1. Almond Mushroom
INSERT INTO mushrooms (id, sub_class, scientific_name, kingdom, family, edibility, description, occurrence, price_pkr, recipes) VALUES (
    1,
    'Almond Mushroom',
    'Agaricus blazei',
    'Fungi',
    'Agaricaceae',
    'Non-poisonous, Edible',
    'Almond mushroom is a well-known edible and medicinal fungus originally found in Brazil. It has a distinct almond-like aroma due to natural compounds like benzaldehyde. The mushroom typically has a brown cap and white stalk with firm flesh. It is rich in nutrients such as proteins, vitamins, and beta-glucans, making it popular for both cooking and health purposes. Due to its taste and texture, it is widely used in soups, sauces, and stir-fry dishes.',
    'Naturally found in Brazil and South America. Cultivated in China, Japan, and some other countries on a limited scale. Rare in the wild, but increasingly cultivated due to demand.',
    'Not commonly available in fresh markets. Estimated prices in dried form: PKR 6,000 to 12,000 per kg. Fresh if locally grown: approximately PKR 1,500 to 3,000 per kg in niche markets. Prices vary because it is mostly imported or specialty-grown.',
    '1. Garlic Butter Almond Mushroom: Slice mushrooms, heat butter and garlic, add mushrooms with salt and pepper, cook 5 to 7 minutes. 2. Almond Mushroom Soup: Boil mushrooms with onion and garlic, add broth and spices, blend and cook for 10 minutes, optionally add cream. 3. Stir-Fry Almond Mushroom: Heat oil, add vegetables, add sliced mushrooms, add soy sauce and spices, cook on high flame. 4. Mushroom Rice: Cook rice separately, fry mushrooms with spices, mix with rice and serve.'
);

