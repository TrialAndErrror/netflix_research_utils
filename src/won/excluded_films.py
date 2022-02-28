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

    return excluded_list
