//deve prendere come riferimento per le opzioni le mosse disponibili 
//in quel momento e deve farlo al posto del turno del nero
//probabilmente da modificare

(async () => {
    try {
        const postTweet = await twitterClient.tweets.createTweet({
            // testo del tweet
            text: "Pronti a fare la vostra mossa?",

            //opzioni di risposta con una poll
            poll: {
                options:[],
                duration_minutes: 10,
            },
        });

        console.dir(postTweet, {
            depth: null,
        });
    } catch (error) {
        console.log(error);
    }
}) ();