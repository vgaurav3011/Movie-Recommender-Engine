import media
import fresh_tomatoes
toy_story = media.Movie("Toy Story",
                        "A story of a boy and his toys that come to life",
                        "https://upload.wikimedia.org/wikipedia/en/1/13/Toy_Story.jpg",
                        "https://www.youtube.com/watch?v=KYz2wyBy3kc")
#print(toy_story.storyline)
avatar = media.Movie("Avatar",
                     "A marine on an alien planet",
                     "https://upload.wikimedia.org/wikipedia/en/b/b0/Avatar-Teaser-Poster.jpg",
                     "https://www.youtube.com/watch?v=5PSNL1qE6VY")
#print(avatar.storyline)
#avatar.show_trailer()
school_of_rock = media.Movie("School of Rock",
                             "Using rock music to learn",
                             "https://upload.wikimedia.org/wikipedia/en/1/11/School_of_Rock_Poster.jpg",
                             "https://www.youtube.com/watch?v=XCwy6lW5Ixc")
ratatouille = media.Movie("Ratatouille",
                          "A rat is a chef in Paris",
                          "https://upload.wikimedia.org/wikipedia/en/5/50/RatatouillePoster.jpg",
                          "https://www.youtube.com/watch?v=c3sBBRxDAqk")
midnight_in_paris = media.Movie("Midnight in Paris",
                                "Going back to meet authors",
                                "https://upload.wikimedia.org/wikipedia/en/9/9f/Midnight_in_Paris_Poster.jpg",
                                "https://www.youtube.com/watch?v=FAfR8omt-CY")
high_school_musical = media.Movie("High School Musical",
                                  "An innocent girl makes out with basketball team captain",
                                  "https://upload.wikimedia.org/wikipedia/en/a/a5/HSMposter.jpg",
                                  "https://www.youtube.com/watch?v=U3G1BogR-68")
interstellar = media.Movie("Interstellar",
                                  "An innocent girl makes out with basketball team captain",
                                  "https://upload.wikimedia.org/wikipedia/en/b/bc/Interstellar_film_poster.jpg",
                                  "https://www.youtube.com/watch?v=zSWdZVtXT7E")
devil_wears_the_prada = media.Movie("The Devil Wears the Prada",
                                  "An innocent girl makes out with basketball team captain",
                                  "https://upload.wikimedia.org/wikipedia/en/e/e7/The_Devil_Wears_Prada_main_onesheet.jpg",
                                  "https://www.youtube.com/watch?v=LG0xYJJbko8")
the_intern = media.Movie("The Intern",
                                  "An innocent girl makes out with basketball team captain",
                                  "https://upload.wikimedia.org/wikipedia/en/c/c9/The_Intern_Poster.jpg",
                                  "https://www.youtube.com/watch?v=ZU3Xban0Y6A")

                                                     
movies = [toy_story, avatar, school_of_rock, ratatouille, midnight_in_paris, high_school_musical, interstellar, devil_wears_the_prada, the_intern]
fresh_tomatoes.open_movies_page(movies)                             