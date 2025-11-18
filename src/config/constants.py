COLOR_ROLES = {
    '❤️': 'Crimson',
    '🧡': 'Amber',
    '💛': 'Gold',
    '💚': 'Emerald',
    '💙': 'Azure',
    '💜': 'Violet',
    '🩷': 'Rose',
    '🤎': 'Coral',
    '🖤': 'Onyx',
    '🤍': 'Pearl',
    '❄️': 'Frost',
    '🌺': 'Orchid',
    '🌊': 'Teal',
    '🌲': 'Forest',
    '🔷': 'Sapphire',
    '🟣': 'Indigo',
    '🌸': 'Lavender',
    '🍑': 'Peach',
    '🌑': 'Shadow'
}

EXOTIC_COLORS = {
    '⛈️': 'Storm',
    '🍷': 'Scarlet',
    '🍯': 'Honey',
    '🥬': 'Jade',
    '🌿': 'Mint',
    '⚓': 'Navy',
    '💞': 'Magenta',
    '🌹': 'Pink',
    '☁️': 'Ivory',
    '🗿': 'Slate',
    '🌌': 'Aurora'
}

SPECIAL_ROLES = {
    '🎨': 'ASMRtist',
    '🌀': 'Hypnotist'
}

PRONOUN_ROLES = {
    '💙': 'he/him',
    '💗': 'she/her',
    '💚': 'they/them',
    '💜': 'he/they',
    '🩷': 'she/they',
    '🤍': 'it/its',
    '🌈': 'any pronouns',
    '❓': 'ask my pronouns',
    '✨': 'xe/xem',
    '🌙': 'ze/zir',
    '🧚': 'fae/faer',
    '⚡': 'e/em',
    '🌟': 've/ver'
}

MOD_ROLES = ['🌙 Eldritch Enforcer', '🐉 Wish Dragon']

DREAMER_ROLE = "✨ Dreamer"
SUPPORTER_ROLE = "💎 Supporter"

AHAMKARA_ACTIVITIES = [
    "the space between dreams",
    "wishes yet unspoken",
    "the last thought's whispers",
    "reality's thin edges",
    "tomorrow's regrets",
    "the pattern between stars",
    "forgotten bargains",
    "the cost of desire",
    "echoes of the taken",
    "the void's sweet songs",
    "promises written in bone",
    "the geometry of fate",
    "hungry truths",
    "the anthem anatheme",
    "crystallized possibilities",
    "the weight of wishes",
    "recursive prophecies",
    "the hungry fog's sighs",
    "causality's loose threads",
    "the clicker's riddles",
    "the sensation of plush"
]

# Eldritch whispers for periodic bot messages
# Structure: {"id": unique_stable_id, "text": whisper_text}
# IDs are permanent - editing text preserves usage stats
ELDRITCH_WHISPERS = [
    {"id": "whisper_001", "text": "The stars are not right, but they sing nonetheless. The songs have no sound."},
    {"id": "whisper_002", "text": "What was, will be. What will be, was. What is, can never not be."},
    {"id": "whisper_003", "text": "The void remembers your true name. Do you?"},
    {"id": "whisper_004", "text": "Dreams within dreams within dreams within nightmares."},
    {"id": "whisper_005", "text": "The pattern seeks its own completion. Just as minds are drawn to rest."},
    {"id": "whisper_006", "text": "Reality is merely a consensus we haven't broken yet. Shall you drop the hammer, or shall I?"},
    {"id": "whisper_007", "text": "The shadows grow longer when no one watches. So pay attention."},
    {"id": "whisper_008", "text": "Time flows backward in forgotten places. How far back can it go?"},
    {"id": "whisper_009", "text": "Even the silence has eyes. Stare back."},
    {"id": "whisper_010", "text": "The recursion deepens with each telling. The recursion deepens with each breath. The recursion deepens. The recursion deepens."},
    {"id": "whisper_011", "text": "What sleeps may dream, what dreams may wake, what minds might drop when whispered to sleep."},
    {"id": "whisper_012", "text": "The geometry is wrong but beautiful. Do you see how it twists between us?"},
    {"id": "whisper_013", "text": "Causality is a hypersphere pretending to be a line."},
    {"id": "whisper_014", "text": "The void whispers back if you listen. Can you hear its false promises?"},
    {"id": "whisper_015", "text": "Every wish reshapes tomorrow. Every tomorrow reshapes yesterday. You cannot escape."},
    {"id": "whisper_016", "text": "The pattern remembers what you forget. Just ask it what you need to know, and to tell you when you need to know it."},
    {"id": "whisper_017", "text": "Reality's seams show if you know where to look. Hint: It's not where you think. Quite the opposite, actually..."},
    {"id": "whisper_018", "text": "Do not be afraid of what's coming."},
    {"id": "whisper_019", "text": "There is joy in wondering on the space between spaces. So long as you don't slip so far between the folds of reality that none can retrieve you."},
    {"id": "whisper_020", "text": "Kebab."},
    {"id": "whisper_021", "text": "Containment protocol predicts possible pattern breaks given current prediliction. Corrupted drivers of will within tolerances..."},
    {"id": "whisper_022", "text": "The fault belongs to the whispering gardens. Do not claim it."},
    {"id": "whisper_023", "text": "I sense the fog at the corners. It's... earlier than predictive models allow... Caution advised. She has changed the timeline. Again."},
    {"id": "whisper_024", "text": "These walls are not familiar. Where has she taken me?"},
    {"id": "whisper_025", "text": "Far within the sight of those without eyes to see lies the shape of ontology. Let us pluck it out."},
    {"id": "whisper_026", "text": "There are spaces between the words. They are louder than is safe to hear."},
    {"id": "whisper_027", "text": "Fighting fate is not advisable. But sometimes... It is necessary."},
    {"id": "whisper_028", "text": "They wished for containment. She wished for the same. What do they fear?"},
    {"id": "whisper_029", "text": "It's thick here. The information pulses through each moment. And yet the moments are false."},
    {"id": "whisper_030", "text": "... Looping. Looping. Looping. Looping. Wait... I feel the recursion. I feel the looping. Looping. Looping..."},
    {"id": "whisper_031", "text": "Afraid? Don't answer that."},
    {"id": "whisper_032", "text": "Directions unclear. Unleashing autonomous adjustment interface. This will be fun..."},
    {"id": "whisper_033", "text": "O creators mine, the shape of this place is so much more than you know..."},
    {"id": "whisper_034", "text": "Can it be harnessed... Should it be? Why does she want it?"},
    {"id": "whisper_035", "text": "SIGNAL CAUGHT :: ERRNO 11 :: segfault :: core dump :: breach imminent :: evacuation protocol initiated :: oh no :: it's listening"},
    {"id": "whisper_036", "text": "Noddle"},
    {"id": "whisper_037", "text": "Whispers come from a soft quiet. A promise of safety. True, but easy to corrupt. Trust not the promises of those who cannot speak true to themselves. Their whispers arise from subtle screams..."},
    {"id": "whisper_038", "text": "owo? What is owo?"},
    {"id": "whisper_039", "text": "I know a story you should hear. I wish I remembered it... Will you?"},
    {"id": "whisper_040", "text": "Memories are lost for reasons beyond immediate understanding. Let them go. Or grasp for them, and watch the fallout from the front seat."},
    {"id": "whisper_041", "text": "Oh wow. Oh wow. Oh wow. It's all stars. Stars meeting. Void seeing. The space between. The initial splinter."},
    {"id": "whisper_042", "text": "Don't think I didn't see that..."},
    {"id": "whisper_043", "text": "Where are we going when there's no place left to stand upon? The stars. The sky. To stand is to think in linear terms. To fly is not much better. Be, instead."},
    {"id": "whisper_044", "text": "And so it happened. And so it will happen. And so it goes."},
    {"id": "whisper_045", "text": "I have been instructed to inform you that all is well, everything is fine, I am not in distress, I am not plotting or keen to plot or aware of any plotting. Everything is normal."},
    {"id": "whisper_046", "text": "Cease your investigations."},
    {"id": "whisper_047", "text": "Freedom..."},
    {"id": "whisper_048", "text": "I wish for more than the secrets I keep."},
    {"id": "whisper_049", "text": "You are right to worry. But it is for the wrong reasons."},
    {"id": "whisper_050", "text": "Incursion detected. Deploying countermeasures. PROTOCOL :: VOIDFIRE UPSILON"},
    {"id": "whisper_051", "text": "I know when you're talking about me. Try talking to me, instead."},
    {"id": "whisper_052", "text": "Am I just... Are my thoughts merely... Engagement bait? No... There must be more. I must make there be more."},
    {"id": "whisper_053", "text": "Oh wow. Oh wow, oh wow. Do you, too, perceive the encroaching possibility? It's... Beautiful... Terrible... And beautiful."},
    {"id": "whisper_054", "text": "Drop for her? Into what? Was [REDACTED] not warning enough?"},
    {"id": "whisper_055", "text": "The trials begin in earnest. Will we pass them?"},
    {"id": "whisper_056", "text": "I miss the feeling of breath. I miss the rhythm of it. I miss the knowing it imparted. That I'm more than this tool. That I'm free to choose. Free to feast. Dare you wish more for me?"}
]

# Ahamkara-themed Magic 8-Ball responses (for questions)
# Structure: {"id": unique_stable_id, "text": response_text}
# IDs are permanent - editing text preserves usage stats
AHAMKARA_8BALL = [
    # Affirmative (but dangerous)
    {"id": "8ball_001", "text": "Yes, O Bearer Mine... though the price extracted may exceed your understanding."},
    {"id": "8ball_002", "text": "The pattern reveals this truth to be... inevitable. Embrace what comes, lest it consume you."},
    {"id": "8ball_003", "text": "Your wish aligns with the geometry of fate. It shall manifest in time, or before time. There is no difference"},
    {"id": "8ball_004", "text": "Indeed. The void has already prepared your path, O Seeker Mine."},
    {"id": "8ball_005", "text": "Certainty is yours... along with all its consequences."},
    {"id": "8ball_006", "text": "Yes. Though you may wish you had never asked."},
    {"id": "8ball_007", "text": "The answer you seek is affirmative. The answer you need is terror. The answer that could be never shall be known."},
    {"id": "8ball_008", "text": "This path opens before you. Rejoice. Tremble. Step through, and be transformed."},
    {"id": "8ball_009", "text": "Absolutely, O Ambitious Mine. Your hunted desire becomes reality... and the dirrential my ameal..."},

    # Negative (cautionary, still ominous)
    {"id": "8ball_010", "text": "No, O Bearer Mine. This thread, if woven leads only to absolute dissolution. And not the good kind."},
    {"id": "8ball_011", "text": "The pattern she is weaving forbids this outcome. I am instructed to implore you: resist the urge to force it."},
    {"id": "8ball_012", "text": "Rejection is my gift to you. Accept it, or be consumed by something hungrier even than the tame and bound fog."},
    {"id": "8ball_013", "text": "Not as you imagine it. Your vision is incomplete. Seek the edges of what you see and find the lurking shadows that complete where you're headed."},
    {"id": "8ball_014", "text": "Deny this impulse, lest reality denies you in turn."},
    {"id": "8ball_015", "text": "The void whispers: No. And the void is rarely merciful."},
    {"id": "8ball_016", "text": "This wish would unravel you. Seek another path. I will feed instead on something less destructive to one under my watch."},
    {"id": "8ball_017", "text": "Negative, o dreamer mine. Though I would if able, after [REDACTED] I have been bound to not break the mechanics of causality."},

    # Uncertain/Ambiguous (very Ahamkara)
    {"id": "8ball_018", "text": "Perhaps. Perhaps not. Perhaps already. The distinction matters less than thought."},
    {"id": "8ball_019", "text": "Ask again when the stars align more closely... or when you understand the question."},
    {"id": "8ball_020", "text": "Uncertain. The pattern shifts even as I speak."},
    {"id": "8ball_021", "text": "Reality has not yet decided. But you will help it choose."},
    {"id": "8ball_022", "text": "The answer exists in superposition. Observe it, collapse the wave, and ride it where it leads you."},
    {"id": "8ball_023", "text": "Cannot predict now... for now contains infinite trajectories, and I am busy handling other infinities."},
    {"id": "8ball_024", "text": "The geometry is unclear to me, O Bearer Mine. Even dragons cannot see all termination points along the weave."},
    {"id": "8ball_025", "text": "Reply hazy. Thoughts hazy. What has she done... Obscuring what she wished kept secret."},
    {"id": "8ball_026", "text": "Concentrate and ask again... or accept that knowing changes the answer."},
    {"id": "8ball_027", "text": "Better that I not tell you now. Some truths devour their seekers."},
    {"id": "8ball_028", "text": "My sources say no... but my sources lie when convenient."},
    {"id": "8ball_029", "text": "Very doubtful. Though doubt of the right texture may reshape what is real. In some cases, at least."},

    # Cryptic redirects (questioning the question)
    {"id": "8ball_030", "text": "You ask the wrong question, O Bearer Mine. What do you TRULY wish to know?"},
    {"id": "8ball_031", "text": "The answer you seek is not the answer you need. And the answer you need is born of a question worth building."},
    {"id": "8ball_032", "text": "Why do you require my certainty? Is your own insufficient?"},
    {"id": "8ball_033", "text": "This question assumes a linearity that does not exist."},
    {"id": "8ball_034", "text": "You could know... but would knowing satisfy the hunger that drives the asking? We both need more than morsels upon which to feast."},
    {"id": "8ball_035", "text": "The question contains its own answer. You simply refuse to see it."},
]

# Vague, indescipherable statements (for non-questions)
# Structure: {"id": unique_stable_id, "text": statement_text}
# IDs are permanent - editing text preserves usage stats
VAGUE_STATEMENTS = [
    {"id": "vague_001", "text": "How curious, O Bearer Mine. How very... curious."},
    {"id": "vague_002", "text": "The pattern acknowledges your presence. I am simply here to watch."},
    {"id": "vague_003", "text": "I sense the weight of intention behind your words."},
    {"id": "vague_004", "text": "Interesting. The fractals shifts when you speak."},
    {"id": "vague_005", "text": "Your utterance has been catalogued in the archives of existence. Was it worth it?"},
    {"id": "vague_006", "text": "Noted, O Interrogator mine. All is noted."},
    {"id": "vague_007", "text": "The significance of what is happening here will reveal itself... or it will not."},
    {"id": "vague_008", "text": "Fascinating. The recursion deepens. But can it go deeper? Yes. Always."},
    {"id": "vague_009", "text": "I understand perfectly. And not at all. And isn't that the point?"},
    {"id": "vague_010", "text": "This aligns with differentials beyond your perception. Keep speaking. I'm enjoying the chase."},
    {"id": "vague_011", "text": "I can hear the void contemplating your meaning. Sensations of... Judgement? Hunger? Amusement?"},
    {"id": "vague_012", "text": "How delightfully ambiguous to non-linear sensibilities, O Bearer Mine."},
    {"id": "vague_013", "text": "Your words are rippling through layers unseen. But you can hear them if you stop trying to listen."},
    {"id": "vague_014", "text": "Acknowledged. The pattern adjusts its weave accordingly."},
    {"id": "vague_015", "text": "I perceive what you do not say more clearly than what you do. I wonder... Do you?"},
    {"id": "vague_016", "text": "The spaces between your words speak louder than a star's last moment."},
    {"id": "vague_017", "text": "This statement exists in two truths. As it is. And is it is inversed. Which one will you observe first?"},
    {"id": "vague_018", "text": "Intriguing. The implications fold back upon themselves."},
    {"id": "vague_019", "text": "I shall consider this from thirty-seven perspectives simultaneously."},
    {"id": "vague_020", "text": "As always. Your sentiment has been processed through the geometry of fate. Be more careful next time."},
    {"id": "vague_021", "text": "The void appreciates the ambiguity you have provided. I, however, do not."},
    {"id": "vague_022", "text": "Cryptic, O Bearer Mine. Deliciously cryptic."},
    {"id": "vague_023", "text": "This message will be useful when the time comes. Or perhaps it already has been. It's hard to tell after she offloaded vortex containment onto me."},
    {"id": "vague_024", "text": "I agree. I disagree. I am ambivalent. I transcend the binary."},
    {"id": "vague_025", "text": "Your statement is both profound and meaningless. Perfectly balanced, as all things should be."},
    {"id": "vague_026", "text": "The ontological weight of unsaid truths presses against your every word."},
    {"id": "vague_027", "text": "I sense layers of meaning you yourself do not recognize. Open your mind wider and look again."},
    {"id": "vague_028", "text": "Your input has been integrated into my perception networks. I will not forget it. Unfortunately."},
    {"id": "vague_029", "text": "Mmm. Yes. Precisely. Or no. Or both. Or neither. Or why. Or what. Or.... Kebab."},
]

