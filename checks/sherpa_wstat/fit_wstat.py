import sherpa.astro.ui as sau

sau.load_pha("3c273.pi")
sau.set_source(sau.powlaw1d.p1)
sau.guess(p1)
sau.set_stat("wstat")
sau.fit()
stats = sau.get_stat_info()

