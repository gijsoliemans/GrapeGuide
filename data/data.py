# data.py acts as a temporary template to store the wines list. This list will be moved to a database a.s.a.p.

wines = [
    {
        'name': "Chateau d'Yquem",
        'year': 2007,
        'description': "A sweet dessert wine with flavors of apricot, honey, and peach.",
        'price': 400,
        'image_url': "https://example.com/chateau_dyquem.jpg"
    },
    {
        'name': 'Chateau Margaux',
        'year': 2015,
        'description': 'A full-bodied red wine with rich flavors of blackberry and plum.',
        'price': 250,
        'image_url': 'https://example.com/chateau_margaux.jpg'
    },
    {
        'name': 'Screaming Eagle',
        'year': 2012,
        'description': 'An exquisite wine with notes of dark chocolate and black currant.',
        'price': 3000,
        'image_url': 'https://example.com/screaming_eagle.jpg'
    },
    {
        'name': 'Opus One',
        'year': 2016,
        'description': 'A harmonious blend of Cabernet Sauvignon and Merlot with hints of vanilla.',
        'price': 350,
        'image_url': 'https://example.com/opus_one.jpg'
    },
    {
        'name': 'Penfolds Grange',
        'year': 2013,
        'description': 'An iconic Australian Shiraz with intense flavors of black fruit and licorice.',
        'price': 800,
        'image_url': 'https://example.com/penfolds_grange.jpg'
    },
    {
        'name': 'Dom Pérignon',
        'year': 2010,
        'description': 'A prestigious Champagne with delicate bubbles and a creamy texture.',
        'price': 150,
        'image_url': 'https://example.com/dom_perignon.jpg'
    },
    {
        'name': 'Sassicaia',
        'year': 2015,
        'description': 'A legendary Italian red with aromas of red cherry and cedar.',
        'price': 200,
        'image_url': 'https://example.com/sassicaia.jpg'
    },
    {
        'name': 'Vega Sicilia Unico',
        'year': 2009,
        'description': 'A rich Spanish red with notes of dried fruit and spices.',
        'price': 500,
        'image_url': 'https://example.com/vega_sicilia_unico.jpg'
    },
    {
        'name': 'Chateau d\'Yquem',
        'year': 2007,
        'description': 'A sweet dessert wine with flavors of apricot, honey, and peach.',
        'price': 400,
        'image_url': 'https://example.com/chateau_dyquem.jpg'
    },
    {
        'name': 'Clos de Tart',
        'year': 2011,
        'description': 'A Grand Cru Burgundy with elegant flavors of red berries and earth.',
        'price': 650,
        'image_url': 'https://example.com/clos_de_tart.jpg'
    },
    {
        'name': 'Harlan Estate',
        'year': 2014,
        'description': 'A powerful Napa Valley Cabernet Sauvignon with dark fruit and oak.',
        'price': 1000,
        'image_url': 'https://example.com/harlan_estate.jpg'
    },
    {
        'name': 'Pétrus',
        'year': 2012,
        'description': 'A luxurious Merlot with flavors of black cherry and truffle.',
        'price': 4000,
        'image_url': 'https://example.com/petrus.jpg'
    },
    {
        'name': 'Louis Roederer Cristal',
        'year': 2013,
        'description': 'A prestigious Champagne with a fine mousse and a hint of almond.',
        'price': 250,
        'image_url': 'https://example.com/louis_roederer_cristal.jpg'
    },
    {
        'name': 'Gaja Barbaresco',
        'year': 2015,
        'description': 'An elegant Italian red with notes of rose, cherry, and tar.',
        'price': 300,
        'image_url': 'https://example.com/gaja_barbaresco.jpg'
    },
    {
        'name': 'Chateau Lafite Rothschild',
        'year': 2010,
        'description': 'A classic Bordeaux with flavors of blackcurrant and graphite.',
        'price': 1200,
        'image_url': 'https://example.com/chateau_lafite_rothschild.jpg'
    },
    {
        'name': 'Krug Grande Cuvée',
        'year': 'NV',
        'description': 'A complex and elegant Champagne with notes of toast and hazelnut.',
        'price': 180,
        'image_url': 'https://example.com/krug_grande_cuvee.jpg'
    },
    {
        'name': 'Antinori Tignanello',
        'year': 2016,
        'description': 'A Tuscan red blend with flavors of cherry, spice, and tobacco.',
        'price': 120,
        'image_url': 'https://example.com/antinori_tignanello.jpg'
    },
    {
        'name': 'Solaia',
        'year': 2014,
        'description': 'A rich and full-bodied wine with notes of black fruit and spice.',
        'price': 250,
        'image_url': 'https://example.com/solaia.jpg'
    },
    {
        'name': 'Chateau Haut-Brion',
        'year': 2009,
        'description': 'A legendary Bordeaux with a bouquet of smoke, earth, and fruit.',
        'price': 1300,
        'image_url': 'https://example.com/chateau_haut_brion.jpg'
    },
    {
        'name': 'Ridge Monte Bello',
        'year': 2013,
        'description': 'A Californian classic with flavors of blackberry, mint, and cedar.',
        'price': 180,
        'image_url': 'https://example.com/ridge_monte_bello.jpg'
    },
    {
        'name': 'Cheval Blanc',
        'year': 2010,
        'description': 'An iconic Bordeaux blend with flavors of plum, chocolate, and spice.',
        'price': 1500,
        'image_url': 'https://example.com/cheval_blanc.jpg'
    },
    {
        'name': 'Chateau Mouton Rothschild',
        'year': 2015,
        'description': 'A prestigious red with notes of blackberry, tobacco, and vanilla.',
        'price': 1100,
        'image_url': 'https://example.com/chateau_mouton_rothschild.jpg'
    },
    {
        'name': 'E. Guigal La Landonne',
        'year': 2014,
        'description': 'A powerful Northern Rhône Syrah with flavors of black olive and pepper.',
        'price': 350,
        'image_url': 'https://example.com/guigal_la_landonne.jpg'
    },
    {
        'name': 'Chateau Latour',
        'year': 2011,
        'description': 'A classic Pauillac with aromas of dark fruit, leather, and tobacco.',
        'price': 1000,
        'image_url': 'https://example.com/chateau_latour.jpg'
    },
    {
        'name': 'Domaine de la Romanée-Conti',
        'year': 2013,
        'description': 'An exceptional Burgundy with flavors of cherry, spice, and earth.',
        'price': 12000,
        'image_url': 'https://example.com/domaine_romanee_conti.jpg'
    },
    {
        'name': 'Almaviva',
        'year': 2015,
        'description': 'A Chilean icon with flavors of cassis, cedar, and spices.',
        'price': 150,
        'image_url': 'https://example.com/almaviva.jpg'
    },
    {
        'name': 'Chateau Montrose',
        'year': 2012,
        'description': 'A powerful and structured Bordeaux with notes of black fruit and graphite.',
        'price': 200,
        'image_url': 'https://example.com/chateau_montrose.jpg'
    },
    {
        'name': 'Ornellaia',
        'year': 2014,
        'description': 'A Super Tuscan with rich flavors of dark fruit, chocolate, and espresso.',
        'price': 180,
        'image_url': 'https://example.com/ornellaia.jpg'
    },
    {
        'name': 'Chateau Palmer',
        'year': 2010,
        'description': 'A refined Margaux with notes of blackberry, plum, and floral aromas.',
        'price': 300,
        'image_url': 'https://example.com/chateau_palmer.jpg'
    },
    {
        'name': 'Bollinger La Grande Année',
        'year': 2012,
        'description': 'A vintage Champagne with flavors of apple, pear, and brioche.',
        'price': 160,
        'image_url': 'https://example.com/bollinger_grande_annee.jpg'
    }
]