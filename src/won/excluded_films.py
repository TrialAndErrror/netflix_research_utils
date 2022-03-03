def get_excluded_films():
    excluded_list = []

    """
    Excluding the following titles because they are shows, not a movies
    """
    non_movie_titles = [
        "Go Dog Go"

    ]

    excluded_list.extend(non_movie_titles)

    """
    Excluding the following movies because they do not have FlixPatrol pages,
    so it is unclear whether they have appeared on a Top 10 list.
    """
    missing_flixpatrol_pages = [
        "Dhamaka",
        "Drive",
        "Sahara",
        "Swallow",
        "The Match",

        "7 años",
        "Ari Eldjárn: Pardon My Icelandic",
        "Bleach",
        "Blood Will Tell",
        "Carlos Ballarta: Furia Ñera",
        "Heroin(e)",
        "Katherine Ryan: Glitter Room",
        "Manhunt",
        "Martin Matte: La vie, la mort...eh la la..!",
        "Mercy",
        "Naked",
        "Park Na-rae: Glamour Warning",
        "Phil Wang: Philly Philly Wang Wang",
        "Point Blank",
        "Ratones Paranoicos: The Band that Rocked Argentina",
        "Sofía Niño de Rivera: Exposed",
        "The Package",
        "The Road to El Camino: Behind the Scenes of El Camino: A Breaking Bad Movie",
        "True: Happy Hearts Day",
        "Us and Them",
        "White Fang",
        "Whitney Cummings: Can I Touch It?"
    ]

    excluded_list.extend(missing_flixpatrol_pages)

    """
    Excluding the following titles because they don't qualify as Netflix films;
    """
    non_movie_titles = [
        'A Family Reunion Christmas',
        'A StoryBots Christmas',
        'A StoryBots Space Adventure',
        'Aggretsuko: We Wish You a Metal Christmas',
        'Altered Carbon: Resleeved',
        'An Unremarkable Christmas',
        'Beat Bugs: All Together Now',
        'Black Mirror: Bandersnatch',
        'Bling Empire - The Afterparty',
        'Bridgerton - The Afterparty',
        'Buddy Thunderstruck: The Maybe Pile',
        'Captain Underpants Epic Choice-o-Rama',
        'Captain Underpants Mega Blissmas',
        'Carmen Sandiego: To Steal or Not to Steal',
        'Chico Bon Bon and the Very Berry Holiday',
        'Club de Cuervos Presents: I, Potro',
        'Cobra Kai - The Afterparty',
        'Dad Stop Embarrassing Me - The Afterparty',
        'Dragons: Rescue Riders: Hunt for the Golden Dragon',
        'Dragons: Rescue Riders: Huttsgalor Holiday',
        'Dragons: Rescue Riders: Secrets of the Songwing',
        'DreamWorks Home: For the Holidays',
        'Fate: The Winx Saga - The Afterparty',
        'Free Rein: The Twelve Neighs of Christmas',
        'Go! Go! Cory Carson: The Chrissy',
        'GO! The Unforgettable Party',
        'Headspace: Unwind Your Mind',
        'Kingdom: Ashin of the North',
        'Making The Billion Dollar Code',
        'Making The Witcher',
        'Making Unorthodox', 'Malibu Rescue',
        'Malibu Rescue: The Next Wave',
        'Marco Polo: One Hundred Eyes',
        'Mighty Express: A Mighty Christmas',
        'My Next Guest with David Letterman and Shah Rukh Khan',
        'Night on Earth: Shot in the Dark',
        'Octonauts & the Caves of Sac Actun',
        'Octonauts & the Great Barrier Reef',
        'Our Planet - Behind The Scenes',
        'Prince of Peoria: A Christmas Moose Miracle',
        'Puss in Book: Trapped in an Epic Tale',
        'Sense8: Creating the World',
        'Shadow and Bone - The Afterparty',
        'Spirit Riding Free: Ride Along Adventure',
        'Spirit Riding Free: Spirit of Christmas',
        'StarBeam: Halloween Hero',
        'Stretch Armstrong: The Breakout',
        'Sugar High',
        'Super Monsters and the Wish Star',
        'Super Monsters Back to School',
        'Super Monsters Furever Friends',
        'Super Monsters Save Christmas',
        'Super Monsters Save Halloween',
        'Super Monsters: Dia de los Monsters',
        'Super Monsters: Once Upon a Rhyme',
        'Super Monsters: The New Class',
        'Swearnet Live',
        'The Circle - The Afterparty',
        'The Crystal Calls Making the Dark Crystal: Age of Resistance',
        'The House of Flowers Presents: The Funeral',
        'The House of Flowers: The Movie',
        'The Last Kids on Earth: Happy Apocalypse to You',
        'The Magic School Bus Rides Again In the Zone',
        'The Magic School Bus Rides Again Kids In Space',
        'The Magic School Bus Rides Again The Frizz Connection',
        'The Netflix Afterparty: The Best Shows of The Worst Year',
        'The Road to El Camino: Behind the Scenes of El Camino: A Breaking Bad Movie',
        'The Spooky Tale of Captain Underpants Hack-a-ween',
        'The Upshaws - The Afterparty',
        'The Witcher: Nightmare of the Wolf',
        'To All the Boys: Always and Forever - The Afterparty',
        'Trailer Park Boys Live at the North Pole',
        'Trese After Dark',
        'True: Friendship Day',
        'True: Grabbleapple Harvest',
        'True: Happy Hearts Day',
        'True: Rainbow Rescue',
        'True: Tricky Treat Day',
        'True: Winter Wishes',
        'True: Wuzzle Wegg Day',
        'Unbreakable Kimmy Schmidt: Kimmy vs. the Reverend'
    ]

    excluded_list.extend(non_movie_titles)

    return excluded_list
