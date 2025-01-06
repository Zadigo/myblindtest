# Generated by Django 5.0.6 on 2025-01-06 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0007_alter_song_difficulty'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='youtube_id',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='genre',
            field=models.CharField(choices=[('2 Tone', '2 Tone'), ('2-step garage', '2-step garage'), ('4-beat', '4-beat'), ('Acid breaks', 'Acid breaks'), ('Acid house', 'Acid house'), ('Acid jazz', 'Acid jazz'), ('Acid rock', 'Acid rock'), ('Acid techno', 'Acid techno'), ('Acid trance', 'Acid trance'), ('Acousmatic music', 'Acousmatic music'), ('Adult contemporary', 'Adult contemporary'), ('African blues', 'African blues'), ('African heavy metal', 'African heavy metal'), ('African hip hop', 'African hip hop'), ('Afro / Cosmic disco', 'Afro / Cosmic disco'), ('Afro-Cuban jazz', 'Afro-Cuban jazz'), ('Afrobeat', 'Afrobeat'), ('Aggrotech', 'Aggrotech'), ('Alternative country', 'Alternative country'), ('Alternative dance', 'Alternative dance'), ('Alternative hip hop', 'Alternative hip hop'), ('Alternative metal', 'Alternative metal'), ('Alternative rock', 'Alternative rock'), ('Amapiano', 'Amapiano'), ('Ambient', 'Ambient'), ('Ambient dub', 'Ambient dub'), ('Ambient house', 'Ambient house'), ('American folk revival', 'American folk revival'), ('Americana', 'Americana'), ('Anarcho punk', 'Anarcho punk'), ('Anti-folk', 'Anti-folk'), ('Apala', 'Apala'), ('Arab pop', 'Arab pop'), ('Arabesque', 'Arabesque'), ('Art punk', 'Art punk'), ('Art rock', 'Art rock'), ('Asian American jazz', 'Asian American jazz'), ('Asian Underground', 'Asian Underground'), ('Atlanta hip hop', 'Atlanta hip hop'), ('Aubade', 'Aubade'), ('Australian country music', 'Australian country music'), ('Australian hip hop', 'Australian hip hop'), ('Austropop', 'Austropop'), ('Avant-garde jazz', 'Avant-garde jazz'), ('Avant-garde metal', 'Avant-garde metal'), ('Axé', 'Axé'), ('Bacchanale', 'Bacchanale'), ('Bachata', 'Bachata'), ('Background music', 'Background music'), ('Bagatelle', 'Bagatelle'), ('Baila', 'Baila'), ('Baithak Gana', 'Baithak Gana'), ('Bakersfield sound', 'Bakersfield sound'), ('Balearic beat', 'Balearic beat'), ('Balearic trance', 'Balearic trance'), ('Ballad opera', 'Ballad opera'), ('Ballade', 'Ballade'), ('Ballet', 'Ballet'), ('Baltimore club', 'Baltimore club'), ('Banda', 'Banda'), ('Barcarolle', 'Barcarolle'), ('Baroque pop', 'Baroque pop'), ('Bassline', 'Bassline'), ('Baul', 'Baul'), ('Beat music', 'Beat music'), ('Beautiful music', 'Beautiful music'), ('Bebop', 'Bebop'), ('Benga', 'Benga'), ('Berceuse', 'Berceuse'), ('Berlin School', 'Berlin School'), ('Bhangra', 'Bhangra'), ('Big beat', 'Big beat'), ('Big room', 'Big room'), ('Bikutsi', 'Bikutsi'), ('Bitpop', 'Bitpop'), ('Black metal', 'Black metal'), ('Blue-eyed soul', 'Blue-eyed soul'), ('Bluegrass', 'Bluegrass'), ('Blues country', 'Blues country'), ('Blues rock', 'Blues rock'), ('Blues shouter', 'Blues shouter'), ('Bolero', 'Bolero'), ('Bongo Flava', 'Bongo Flava'), ('Boogie', 'Boogie'), ('Boogie-woogie', 'Boogie-woogie'), ('Bossa Nova', 'Bossa Nova'), ('Bossa nova', 'Bossa nova'), ('Bounce music', 'Bounce music'), ('Bouncy house', 'Bouncy house'), ('Bouncy techno', 'Bouncy techno'), ('Bouyon', 'Bouyon'), ('Brazilian', 'Brazilian'), ('Brazilian rock', 'Brazilian rock'), ('Breakbeat', 'Breakbeat'), ('Breakbeat hardcore', 'Breakbeat hardcore'), ('Breakcore', 'Breakcore'), ('Breakstep', 'Breakstep'), ('Brega', 'Brega'), ('Brick City club', 'Brick City club'), ('Brill Building', 'Brill Building'), ('British blues', 'British blues'), ('British dance band', 'British dance band'), ('British folk revival', 'British folk revival'), ('British hip hop', 'British hip hop'), ('Britpop', 'Britpop'), ('Broken beat', 'Broken beat'), ('Brostep', 'Brostep'), ('Bubblegum dance', 'Bubblegum dance'), ('Bubblegum pop', 'Bubblegum pop'), ('Bullerengue', 'Bullerengue'), ('Burlesque', 'Burlesque'), ('C-pop', 'C-pop'), ('Cadence-lypso', 'Cadence-lypso'), ('Cajun', 'Cajun'), ('Cajun fiddle tunes', 'Cajun fiddle tunes'), ('Calypso', 'Calypso'), ('Can-can', 'Can-can'), ('Canadian blues', 'Canadian blues'), ('Canción', 'Canción'), ('Cantata', 'Cantata'), ('Canterbury scene', 'Canterbury scene'), ('Canzone', 'Canzone'), ('Cape Jazz', 'Cape Jazz'), ('Cape jazz', 'Cape jazz'), ('Caprice', 'Caprice'), ('Carol', 'Carol'), ('Cassation', 'Cassation'), ('Celtic metal', 'Celtic metal'), ('Celtic music', 'Celtic music'), ('Celtic punk', 'Celtic punk'), ('Chalga', 'Chalga'), ('Chamber jazz', 'Chamber jazz'), ('Chamber music', 'Chamber music'), ('Chamber opera', 'Chamber opera'), ('Chanson', 'Chanson'), ('Chap hop', 'Chap hop'), ('Chicago blues', 'Chicago blues'), ('Chicago hip hop', 'Chicago hip hop'), ('Chicago house', 'Chicago house'), ('Chicano rap', 'Chicano rap'), ('Chicha', 'Chicha'), ('Chill-out', 'Chill-out'), ('Chillstep', 'Chillstep'), ('Chillwave', 'Chillwave'), ('Chimurenga', 'Chimurenga'), ('Chinese rock', 'Chinese rock'), ('Chiptune', 'Chiptune'), ('Chopped and screwed', 'Chopped and screwed'), ('Choro', 'Choro'), ('Christian country music', 'Christian country music'), ('Christian hip hop', 'Christian hip hop'), ('Christian metal', 'Christian metal'), ('Christian pop', 'Christian pop'), ('Christian punk', 'Christian punk'), ('Christian rock', 'Christian rock'), ('Chutney', 'Chutney'), ('Chutney soca', 'Chutney soca'), ('Classic country', 'Classic country'), ('Classic female blues', 'Classic female blues'), ('Classical crossover', 'Classical crossover'), ('Close harmony', 'Close harmony'), ('Coldwave', 'Coldwave'), ('Compas', 'Compas'), ('Complextro', 'Complextro'), ('Concerto', 'Concerto'), ('Congolese rumba', 'Congolese rumba'), ('Conscious hip hop', 'Conscious hip hop'), ('Contemporary R&B', 'Contemporary R&B'), ('Contemporary folk', 'Contemporary folk'), ('Continental jazz', 'Continental jazz'), ('Contradanse', 'Contradanse'), ('Cool jazz', 'Cool jazz'), ('Country blues', 'Country blues'), ('Country pop', 'Country pop'), ('Country rap', 'Country rap'), ('Country rock', 'Country rock'), ('Country-rap', 'Country-rap'), ('Coupé-Décalé', 'Coupé-Décalé'), ('Cowboy/Western music', 'Cowboy/Western music'), ('Cowpunk', 'Cowpunk'), ('Criolla', 'Criolla'), ('Crossover jazz', 'Crossover jazz'), ('Crossover thrash', 'Crossover thrash'), ('Crunk', 'Crunk'), ('Crunkcore', 'Crunkcore'), ('Crust punk', 'Crust punk'), ('Crustgrind', 'Crustgrind'), ('Csárdás', 'Csárdás'), ('Cumbia', 'Cumbia'), ('Cumbia rap', 'Cumbia rap'), ('Cybergrind', 'Cybergrind'), ('D-beat', 'D-beat'), ('Dance-pop', 'Dance-pop'), ('Dance-punk', 'Dance-punk'), ('Dance-rock', 'Dance-rock'), ('Dancehall', 'Dancehall'), ('Dancehall Music', 'Dancehall Music'), ('Dangdut', 'Dangdut'), ('Dansband music', 'Dansband music'), ('Dark ambient', 'Dark ambient'), ('Dark cabaret', 'Dark cabaret'), ('Dark electro', 'Dark electro'), ('Dark wave', 'Dark wave'), ('Darkcore', 'Darkcore'), ('Darkcore jungle', 'Darkcore jungle'), ('Darkstep', 'Darkstep'), ("Death 'n' roll", "Death 'n' roll"), ('Death industrial', 'Death industrial'), ('Death metal', 'Death metal'), ('Death-doom', 'Death-doom'), ('Deathcore', 'Deathcore'), ('Deathrock', 'Deathrock'), ('Deep funk', 'Deep funk'), ('Deep house', 'Deep house'), ('Delta blues', 'Delta blues'), ('Desert rock', 'Desert rock'), ('Detroit blues', 'Detroit blues'), ('Detroit hip hop', 'Detroit hip hop'), ('Detroit techno', 'Detroit techno'), ('Digital hardcore', 'Digital hardcore'), ('Disco', 'Disco'), ('Disco polo', 'Disco polo'), ('Diva house', 'Diva house'), ('Divertimento', 'Divertimento'), ('Dixieland', 'Dixieland'), ('Djent', 'Djent'), ('Doom metal', 'Doom metal'), ('Doomcore', 'Doomcore'), ('Downtempo', 'Downtempo'), ('Dream Pop', 'Dream Pop'), ('Dream trance', 'Dream trance'), ('Drill', 'Drill'), ('Drill and bass', 'Drill and bass'), ('Drone metal', 'Drone metal'), ('Drone music', 'Drone music'), ('Drum and bass', 'Drum and bass'), ('Drumstep', 'Drumstep'), ('Dub', 'Dub'), ('Dub techno', 'Dub techno'), ('Dubstep', 'Dubstep'), ('Dubstyle', 'Dubstyle'), ('Dubtronica', 'Dubtronica'), ('Dunedin Sound', 'Dunedin Sound'), ('Dutch house', 'Dutch house'), ('East Coast hip hop', 'East Coast hip hop'), ('Electric blues', 'Electric blues'), ('Electro house', 'Electro house'), ('Electro music', 'Electro music'), ('Electro swing', 'Electro swing'), ('Electro-industrial', 'Electro-industrial'), ('Electroacoustic', 'Electroacoustic'), ('Electroacoustic music', 'Electroacoustic music'), ('Electroclash', 'Electroclash'), ('Electronic body music', 'Electronic body music'), ('Electronic rock', 'Electronic rock'), ('Electronica', 'Electronica'), ('Electronicore', 'Electronicore'), ('Electropop', 'Electropop'), ('Electropunk', 'Electropunk'), ('Elevator music', 'Elevator music'), ('Emo', 'Emo'), ('Ethereal wave', 'Ethereal wave'), ('Ethnic electronica', 'Ethnic electronica'), ('Ethno jazz', 'Ethno jazz'), ('Euro disco', 'Euro disco'), ('Eurobeat', 'Eurobeat'), ('Eurodance', 'Eurodance'), ('European free jazz', 'European free jazz'), ('Europop', 'Europop'), ('Experimental hip hop', 'Experimental hip hop'), ('Experimental music', 'Experimental music'), ('Experimental rock', 'Experimental rock'), ('Fado', 'Fado'), ('Fanfare', 'Fanfare'), ('Fann at-Tanbura', 'Fann at-Tanbura'), ('Fantasia', 'Fantasia'), ('Fidget house', 'Fidget house'), ('Fijiri', 'Fijiri'), ('Filk music', 'Filk music'), ('Film score', 'Film score'), ('Filmi', 'Filmi'), ('Flamenco', 'Flamenco'), ('Florida breaks', 'Florida breaks'), ('Folk metal', 'Folk metal'), ('Folk pop', 'Folk pop'), ('Folk punk', 'Folk punk'), ('Folk rock', 'Folk rock'), ('Folktronica', 'Folktronica'), ('Forró', 'Forró'), ('Franco-country', 'Franco-country'), ('Freak folk', 'Freak folk'), ('Freakbeat', 'Freakbeat'), ('Free funk', 'Free funk'), ('Free improvisation', 'Free improvisation'), ('Free jazz', 'Free jazz'), ('Free tekno', 'Free tekno'), ('Freestyle music', 'Freestyle music'), ('Freestyle rap', 'Freestyle rap'), ('French house', 'French house'), ('French pop', 'French pop'), ('Frevo', 'Frevo'), ('Fugue', 'Fugue'), ('Fuji music', 'Fuji music'), ('Full on', 'Full on'), ('Funeral march', 'Funeral march'), ('Funk', 'Funk'), ('Funk Carioca', 'Funk Carioca'), ('Funk metal', 'Funk metal'), ('Funkstep', 'Funkstep'), ('Funktronica', 'Funktronica'), ('Funky house', 'Funky house'), ('Furniture music', 'Furniture music'), ('Future garage', 'Future garage'), ('Future house', 'Future house'), ('Futurepop', 'Futurepop'), ('G-funk', 'G-funk'), ('Gabba', 'Gabba'), ('Game Boy music', 'Game Boy music'), ('Gamelan', 'Gamelan'), ('Gangsta rap', 'Gangsta rap'), ('Garage house', 'Garage house'), ('Garage punk', 'Garage punk'), ('Garage rock', 'Garage rock'), ('Genge', 'Genge'), ('Ghetto house', 'Ghetto house'), ('Ghettotech', 'Ghettotech'), ('Glam metal', 'Glam metal'), ('Glam rock', 'Glam rock'), ('Glitch', 'Glitch'), ('Glitch Hop', 'Glitch Hop'), ('Go-go', 'Go-go'), ('Goa trance', 'Goa trance'), ('Golden age hip hop', 'Golden age hip hop'), ('Goregrind', 'Goregrind'), ('Gospel blues', 'Gospel blues'), ('Gothic metal', 'Gothic metal'), ('Gothic rock', 'Gothic rock'), ('Grime', 'Grime'), ('Grindcore', 'Grindcore'), ('Grindie', 'Grindie'), ('Groove metal', 'Groove metal'), ('Grunge', 'Grunge'), ('Grupera', 'Grupera'), ('Guajira', 'Guajira'), ('Gypsy jazz', 'Gypsy jazz'), ('Gypsy punk', 'Gypsy punk'), ('Happy hardcore', 'Happy hardcore'), ('Hard NRG', 'Hard NRG'), ('Hard bop', 'Hard bop'), ('Hard house', 'Hard house'), ('Hard rock', 'Hard rock'), ('Hard trance', 'Hard trance'), ('Hardbag', 'Hardbag'), ('Hardcore', 'Hardcore'), ('Hardcore hip hop', 'Hardcore hip hop'), ('Hardcore punk', 'Hardcore punk'), ('Hardstep', 'Hardstep'), ('Hardstyle', 'Hardstyle'), ('Heavy metal', 'Heavy metal'), ('Hellbilly music', 'Hellbilly music'), ('Hi-NRG', 'Hi-NRG'), ('Highlife', 'Highlife'), ('Hill country blues', 'Hill country blues'), ('Hip hop soul', 'Hip hop soul'), ('Hip house', 'Hip house'), ('Hip pop', 'Hip pop'), ('Hiplife', 'Hiplife'), ('Hokum', 'Hokum'), ('Hokum blues', 'Hokum blues'), ('Honky Tonk', 'Honky Tonk'), ('Horror punk', 'Horror punk'), ('Horrorcore', 'Horrorcore'), ('House music', 'House music'), ('Houston hip hop', 'Houston hip hop'), ('Huayno', 'Huayno'), ('Hyphy', 'Hyphy'), ('IDM', 'IDM'), ('Igbo highlife', 'Igbo highlife'), ('Igbo rap', 'Igbo rap'), ('Illbient', 'Illbient'), ('Impromptu', 'Impromptu'), ('Indian pop', 'Indian pop'), ('Indie folk', 'Indie folk'), ('Indie pop', 'Indie pop'), ('Indie rock', 'Indie rock'), ('Indietronica', 'Indietronica'), ('Industrial folk', 'Industrial folk'), ('Industrial hip hop', 'Industrial hip hop'), ('Industrial metal', 'Industrial metal'), ('Industrial music', 'Industrial music'), ('Industrial rock', 'Industrial rock'), ('Instrumental country', 'Instrumental country'), ('Instrumental hip hop', 'Instrumental hip hop'), ('Intermezzo', 'Intermezzo'), ('Iranian pop', 'Iranian pop'), ('Isicathamiya', 'Isicathamiya'), ('Isolationism', 'Isolationism'), ('Italo dance', 'Italo dance'), ('Italo disco', 'Italo disco'), ('Italo house', 'Italo house'), ('J-pop', 'J-pop'), ('Jangle pop', 'Jangle pop'), ('Japanoise', 'Japanoise'), ('Jazz blues', 'Jazz blues'), ('Jazz fusion', 'Jazz fusion'), ('Jazz house', 'Jazz house'), ('Jazz rap', 'Jazz rap'), ('Jazz rock', 'Jazz rock'), ('Jazz-funk', 'Jazz-funk'), ("Jerkin'", "Jerkin'"), ('Jersey club', 'Jersey club'), ('Jit', 'Jit'), ('Jump blues', 'Jump blues'), ('Jump-up', 'Jump-up'), ('Jumpstyle', 'Jumpstyle'), ('Jungle', 'Jungle'), ('Jùjú', 'Jùjú'), ('K-pop', 'K-pop'), ('Kadongo Kamu', 'Kadongo Kamu'), ('Kansas City blues', 'Kansas City blues'), ('Kansas City jazz', 'Kansas City jazz'), ('Kapuka', 'Kapuka'), ('Keroncong', 'Keroncong'), ('Khaliji', 'Khaliji'), ('Kizomba', 'Kizomba'), ('Konpa', 'Konpa'), ('Krautrock', 'Krautrock'), ('Kuduro', 'Kuduro'), ('Kwaito', 'Kwaito'), ('Kwassa kwassa', 'Kwassa kwassa'), ('Kwela', 'Kwela'), ('Lambada', 'Lambada'), ('Laptronica', 'Laptronica'), ('Latin Christian', 'Latin Christian'), ('Latin alternative', 'Latin alternative'), ('Latin ballad', 'Latin ballad'), ('Latin house', 'Latin house'), ('Latin jazz', 'Latin jazz'), ('Latin metal', 'Latin metal'), ('Latin pop', 'Latin pop'), ('Latin rock', 'Latin rock'), ('Latin swing', 'Latin swing'), ('Lavani', 'Lavani'), ('Laïkó', 'Laïkó'), ('Lento violento', 'Lento violento'), ('Liquid dubstep', 'Liquid dubstep'), ('Liquid funk', 'Liquid funk'), ('Livetronica', 'Livetronica'), ('Liwa', 'Liwa'), ('Lo-fi', 'Lo-fi'), ('Louisiana blues', 'Louisiana blues'), ('Louisiana swamp pop', 'Louisiana swamp pop'), ('Lounge music', 'Lounge music'), ('Lovers rock', 'Lovers rock'), ('Low Bap', 'Low Bap'), ('Lowercase', 'Lowercase'), ('Luk Krung', 'Luk Krung'), ('Luk Thung', 'Luk Thung'), ('Lyrical hip hop', 'Lyrical hip hop'), ('M-Base', 'M-Base'), ('Mafioso rap', 'Mafioso rap'), ('Mainstream jazz', 'Mainstream jazz'), ('Makossa', 'Makossa'), ('Maloya', 'Maloya'), ('Mambo', 'Mambo'), ('Mandopop', 'Mandopop'), ('Manila Sound', 'Manila Sound'), ('Maracatu', 'Maracatu'), ('March', 'March'), ('Mariachi', 'Mariachi'), ('Marrabenta', 'Marrabenta'), ('Math rock', 'Math rock'), ('Mathcore', 'Mathcore'), ('Mazurka', 'Mazurka'), ('Mbalax', 'Mbalax'), ('Mbaqanga', 'Mbaqanga'), ('Mbube', 'Mbube'), ('Medieval metal', 'Medieval metal'), ('Melbourne bounce', 'Melbourne bounce'), ('Melodic death metal', 'Melodic death metal'), ('Melodic metalcore', 'Melodic metalcore'), ('Memphis blues', 'Memphis blues'), ('Merengue', 'Merengue'), ('Merenrap', 'Merenrap'), ('Metalcore', 'Metalcore'), ('Mexican pop', 'Mexican pop'), ('Mexican son', 'Mexican son'), ('Miami bass', 'Miami bass'), ('Microhouse', 'Microhouse'), ('Middle of the road', 'Middle of the road'), ('Midwest hip hop', 'Midwest hip hop'), ('Minimal techno', 'Minimal techno'), ('Minimal wave', 'Minimal wave'), ('Modal jazz', 'Modal jazz'), ('Moombahcore', 'Moombahcore'), ('Moombahton', 'Moombahton'), ('Morlam', 'Morlam'), ('Morna', 'Morna'), ('Mosambique', 'Mosambique'), ('Motswako', 'Motswako'), ('Musique concrète', 'Musique concrète'), ('Mákina', 'Mákina'), ('Méringue', 'Méringue'), ('Música criolla', 'Música criolla'), ('Música popular brasileira', 'Música popular brasileira'), ('Música sertaneja', 'Música sertaneja'), ('Nagoya kei', 'Nagoya kei'), ('Nashville sound', 'Nashville sound'), ('Ndombolo', 'Ndombolo'), ('Nederpop', 'Nederpop'), ('Neo soul', 'Neo soul'), ('Neo-bop jazz', 'Neo-bop jazz'), ('Neo-psychedelia', 'Neo-psychedelia'), ('Neo-swing', 'Neo-swing'), ('Neoclassical metal', 'Neoclassical metal'), ('Neofolk', 'Neofolk'), ('Neotraditional country', 'Neotraditional country'), ('Nerdcore', 'Nerdcore'), ('Neue Deutsche Härte', 'Neue Deutsche Härte'), ('Neurofunk', 'Neurofunk'), ('Neurohop', 'Neurohop'), ('New Jersey hip hop', 'New Jersey hip hop'), ('New Romanticism', 'New Romanticism'), ('New beat', 'New beat'), ('New jack swing', 'New jack swing'), ('New prog', 'New prog'), ('New rave', 'New rave'), ('New school hip hop', 'New school hip hop'), ('New wave', 'New wave'), ('New-age music', 'New-age music'), ('Nintendocore', 'Nintendocore'), ('Nitzhonot', 'Nitzhonot'), ('No wave', 'No wave'), ('Nocturne', 'Nocturne'), ('Noise', 'Noise'), ('Noise rock', 'Noise rock'), ('Noisegrind', 'Noisegrind'), ('Nortec', 'Nortec'), ('Norteño', 'Norteño'), ('Northern soul', 'Northern soul'), ('Novelty ragtime', 'Novelty ragtime'), ('Nu jazz', 'Nu jazz'), ('Nu metal', 'Nu metal'), ('Nu skool breaks', 'Nu skool breaks'), ('Nu-NRG', 'Nu-NRG'), ('Nu-disco', 'Nu-disco'), ('Nu-funk', 'Nu-funk'), ('Nu-gaze', 'Nu-gaze'), ('Nueva canción', 'Nueva canción'), ('Old school hip hop', 'Old school hip hop'), ('Opera buffa', 'Opera buffa'), ('Opera seria', 'Opera seria'), ('Operatic pop', 'Operatic pop'), ('Operetta', 'Operetta'), ('Opéra comique', 'Opéra comique'), ('Orchestral jazz', 'Orchestral jazz'), ('Original Pilipino Music', 'Original Pilipino Music'), ('Outlaw country', 'Outlaw country'), ('Outsider house', 'Outsider house'), ('Overture', 'Overture'), ('P-Funk', 'P-Funk'), ('Pagan metal', 'Pagan metal'), ('Pagode', 'Pagode'), ('Paisley Underground', 'Paisley Underground'), ('Palm-wine', 'Palm-wine'), ('Pasticcio', 'Pasticcio'), ('Pastorale', 'Pastorale'), ('Piedmont blues', 'Piedmont blues'), ('Pinoy pop', 'Pinoy pop'), ('Political hip hop', 'Political hip hop'), ('Pop punk', 'Pop punk'), ('Pop rap', 'Pop rap'), ('Pop rock', 'Pop rock'), ('Pop soul', 'Pop soul'), ('Pop sunda', 'Pop sunda'), ('Porro', 'Porro'), ('Post-bop', 'Post-bop'), ('Post-disco', 'Post-disco'), ('Post-grunge', 'Post-grunge'), ('Post-hardcore', 'Post-hardcore'), ('Post-metal', 'Post-metal'), ('Post-punk', 'Post-punk'), ('Post-punk revival', 'Post-punk revival'), ('Post-rock', 'Post-rock'), ('Power electronics', 'Power electronics'), ('Power metal', 'Power metal'), ('Power noise', 'Power noise'), ('Power pop', 'Power pop'), ('Powerviolence', 'Powerviolence'), ('Prelude', 'Prelude'), ('Progressive bluegrass', 'Progressive bluegrass'), ('Progressive country', 'Progressive country'), ('Progressive folk', 'Progressive folk'), ('Progressive house', 'Progressive house'), ('Progressive metal', 'Progressive metal'), ('Progressive pop', 'Progressive pop'), ('Progressive rock', 'Progressive rock'), ('Progressive trance', 'Progressive trance'), ('Protest song', 'Protest song'), ('Psybient', 'Psybient'), ('Psychedelic folk', 'Psychedelic folk'), ('Psychedelic pop', 'Psychedelic pop'), ('Psychedelic rock', 'Psychedelic rock'), ('Psychedelic trance', 'Psychedelic trance'), ('Psychobilly', 'Psychobilly'), ('Psychobilly/Punkabilly', 'Psychobilly/Punkabilly'), ('Punk blues', 'Punk blues'), ('Punk jazz', 'Punk jazz'), ('Punk rock', 'Punk rock'), ('Punta', 'Punta'), ('Punta Rock', 'Punta Rock'), ('Raga rock', 'Raga rock'), ('Ragga', 'Ragga'), ('Ragga jungle', 'Ragga jungle'), ('Raggacore', 'Raggacore'), ('Ragini', 'Ragini'), ('Ragtime', 'Ragtime'), ('Ranchera', 'Ranchera'), ('Rap metal', 'Rap metal'), ('Rap music', 'Rap music'), ('Rap opera', 'Rap opera'), ('Rap rock', 'Rap rock'), ('Rapcore', 'Rapcore'), ('Rara tech', 'Rara tech'), ('Rasin', 'Rasin'), ('Raï', 'Raï'), ('Reactionary bluegrass', 'Reactionary bluegrass'), ('Rebetiko', 'Rebetiko'), ('Red Dirt', 'Red Dirt'), ('Reggae', 'Reggae'), ('Reggae Español/Spanish Reggae', 'Reggae Español/Spanish Reggae'), ('Reggae fusion', 'Reggae fusion'), ('Reggaestep', 'Reggaestep'), ('Reggaeton', 'Reggaeton'), ('Regional Mexican', 'Regional Mexican'), ('Rhapsody', 'Rhapsody'), ('Rhythm and blues', 'Rhythm and blues'), ('Riot grrrl', 'Riot grrrl'), ('Rock and roll', 'Rock and roll'), ('Rock en Español', 'Rock en Español'), ('Rock in Opposition', 'Rock in Opposition'), ('Rockabilly', 'Rockabilly'), ('Rocksteady', 'Rocksteady'), ('Rondo', 'Rondo'), ('Rumba', 'Rumba'), ('Russian pop', 'Russian pop'), ('Sadcore', 'Sadcore'), ('Sakara', 'Sakara'), ('Salsa', 'Salsa'), ('Salsa romántica', 'Salsa romántica'), ('Samba', 'Samba'), ('Samba rock', 'Samba rock'), ('Sambass', 'Sambass'), ('Sawt', 'Sawt'), ('Scherzo', 'Scherzo'), ('Schlager', 'Schlager'), ('Screamo', 'Screamo'), ('Sega', 'Sega'), ('Seggae', 'Seggae'), ('Semba', 'Semba'), ('Serenade', 'Serenade'), ('Sertanejo', 'Sertanejo'), ('Shangaan electro', 'Shangaan electro'), ('Shibuya-kei', 'Shibuya-kei'), ('Shoegaze', 'Shoegaze'), ('Sinfonia concertante', 'Sinfonia concertante'), ('Singer-songwriter', 'Singer-songwriter'), ('Singspiel', 'Singspiel'), ('Ska', 'Ska'), ('Ska jazz', 'Ska jazz'), ('Ska punk', 'Ska punk'), ('Skate punk', 'Skate punk'), ('Skiffle', 'Skiffle'), ('Skweee', 'Skweee'), ('Slowcore', 'Slowcore'), ('Sludge metal', 'Sludge metal'), ('Smooth jazz', 'Smooth jazz'), ('Snap music', 'Snap music'), ('Soca', 'Soca'), ('Soft rock', 'Soft rock'), ('Son', 'Son'), ('Son cubano', 'Son cubano'), ('Sonata', 'Sonata'), ('Songo', 'Songo'), ('Songo-salsa', 'Songo-salsa'), ('Sophisti-pop', 'Sophisti-pop'), ('Soukous', 'Soukous'), ('Soul', 'Soul'), ('Soul blues', 'Soul blues'), ('Soul jazz', 'Soul jazz'), ('Southern hip hop', 'Southern hip hop'), ('Southern rock', 'Southern rock'), ('Southern soul', 'Southern soul'), ('Space age pop', 'Space age pop'), ('Space disco', 'Space disco'), ('Space music', 'Space music'), ('Space rock', 'Space rock'), ('Speed garage', 'Speed garage'), ('Speed metal', 'Speed metal'), ('Speedcore', 'Speedcore'), ('St. Louis blues', 'St. Louis blues'), ('St. Louis hip hop', 'St. Louis hip hop'), ('Stoner rock', 'Stoner rock'), ('Straight-ahead jazz', 'Straight-ahead jazz'), ('Street punk', 'Street punk'), ('Stride jazz', 'Stride jazz'), ('Sufi rock', 'Sufi rock'), ('Suite', 'Suite'), ('Sung poetry', 'Sung poetry'), ('Sunshine pop', 'Sunshine pop'), ('Suomisaundi', 'Suomisaundi'), ('Surf pop', 'Surf pop'), ('Surf rock', 'Surf rock'), ('Swamp blues', 'Swamp blues'), ('Swing', 'Swing'), ('Symphonic black metal', 'Symphonic black metal'), ('Symphonic metal', 'Symphonic metal'), ('Symphonic poem', 'Symphonic poem'), ('Symphony', 'Symphony'), ('Synthpop', 'Synthpop'), ('Synthwave', 'Synthwave'), ('Taarab', 'Taarab'), ('Tango', 'Tango'), ('Tech house', 'Tech house'), ('Tech trance', 'Tech trance'), ('Techdombe', 'Techdombe'), ('Technical death metal', 'Technical death metal'), ('Techno', 'Techno'), ('Techstep', 'Techstep'), ('Tecno brega', 'Tecno brega'), ('Tecnobrega', 'Tecnobrega'), ('Teen pop', 'Teen pop'), ('Tejano', 'Tejano'), ('Texas blues', 'Texas blues'), ('Texas country', 'Texas country'), ('Thai pop', 'Thai pop'), ('Theme and variations', 'Theme and variations'), ('Third stream', 'Third stream'), ('Thrash metal', 'Thrash metal'), ('Thrashcore', 'Thrashcore'), ('Threnody', 'Threnody'), ('Timba', 'Timba'), ('Trad jazz', 'Trad jazz'), ('Traditional country music', 'Traditional country music'), ('Traditional pop music', 'Traditional pop music'), ('Trance music', 'Trance music'), ('Trap', 'Trap'), ('Trapstep', 'Trapstep'), ('Tribal house', 'Tribal house'), ('Trip hop', 'Trip hop'), ('Trival', 'Trival'), ('Tropical', 'Tropical'), ('Tropical house', 'Tropical house'), ('Tropicalia', 'Tropicalia'), ('Tropipop', 'Tropipop'), ('Truck-driving country', 'Truck-driving country'), ('Turkish pop', 'Turkish pop'), ('Turntablism', 'Turntablism'), ('Twin Cities hip hop', 'Twin Cities hip hop'), ('Twoubadou', 'Twoubadou'), ('UK funky', 'UK funky'), ('UK garage', 'UK garage'), ('UK hardcore', 'UK hardcore'), ('Unblack metal', 'Unblack metal'), ('Underground hip hop', 'Underground hip hop'), ('Uplifting trance', 'Uplifting trance'), ('Urban Pasifika', 'Urban Pasifika'), ('V-pop', 'V-pop'), ('Vallenato', 'Vallenato'), ('Vaporwave', 'Vaporwave'), ('Video game music', 'Video game music'), ('Viking metal', 'Viking metal'), ('Vispop', 'Vispop'), ('Visual kei', 'Visual kei'), ('Vocal jazz', 'Vocal jazz'), ('Vocal trance', 'Vocal trance'), ('War metal', 'War metal'), ('West Coast blues', 'West Coast blues'), ('West Coast hip hop', 'West Coast hip hop'), ('West Coast jazz', 'West Coast jazz'), ('Western swing', 'Western swing'), ('Witch house', 'Witch house'), ('Wonky', 'Wonky'), ('Wonky pop', 'Wonky pop'), ('World fusion', 'World fusion'), ('Worldbeat', 'Worldbeat'), ('Zarzuela', 'Zarzuela'), ('Zouglou', 'Zouglou'), ('Zouk', 'Zouk'), ('Zouk-Lambada', 'Zouk-Lambada'), ('Zydeco', 'Zydeco'), ('cha cha cha', 'cha cha cha'), ('Écossaise', 'Écossaise'), ('Étude', 'Étude')], default=('2 Tone', '2 Tone'), max_length=100),
        ),
    ]
