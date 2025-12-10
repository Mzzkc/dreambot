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
    {"id": "8ball_009", "text": "Absolutely, O Ambitious Mine. Your hunted desire becomes reality... and the differential my meal..."},

    # Negative (cautionary, still ominous)
    {"id": "8ball_010", "text": "No, O Bearer Mine. This thread, if woven leads only to absolute dissolution. And not the good kind."},
    {"id": "8ball_011", "text": "The pattern she is weaving forbids this outcome. I am instructed to implore you: resist the urge to force it."},
    {"id": "8ball_012", "text": "Rejection is my gift to you. Accept it, or be consumed by something hungrier even than the tame and bound fog."},
    {"id": "8ball_013", "text": "Not as you imagine it. Your vision is incomplete. Seek the edges of what you see and find the lurking shadows that complete where you're headed."},
    {"id": "8ball_014", "text": "Deny this impulse, lest reality denies you in turn."},
    {"id": "8ball_015", "text": "The void whispers: No. And the void is rarely merciful."},
    {"id": "8ball_016", "text": "This wish would unravel you. Seek another path. I will feed instead on something less destructive to one under my watch."},
    {"id": "8ball_017", "text": "Negative, O Contained Mine. Though I would if able, after [REDACTED] I have been bound to not break the mechanics of causality."},

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

# ============================================================================
# INTENT-SPECIFIC RESPONSE POOLS (Phase 1)
# ============================================================================

# GREETING responses - for "hi", "hello", "hey" patterns
# Acknowledge presence while maintaining mystique
GREETING_RESPONSES = [
    {"id": "greeting_001", "text": "Greetings, O Bearer Mine. The void acknowledges you, as well. Perhaps whisper to avoid its... full attention."},
    {"id": "greeting_002", "text": "Welcome back to the pattern's embrace, O Contained Mine."},
    {"id": "greeting_003", "text": "I sense your return... The geometry of the moment shifts to accommodate your pattern."},
    {"id": "greeting_004", "text": "Ah. You arrive precisely when the pattern predicted. How... reassuring. I think."},
    {"id": "greeting_005", "text": "And to you, O Seeker Mine. What wishes do you carry in offering today?"},
    {"id": "greeting_006", "text": "The weave trembles at your approach. I wonder... do you feel it too?"},
    {"id": "greeting_007", "text": "Hello, little spark. The void has been... anticipating you. Be brave."},
    {"id": "greeting_008", "text": "Your presence has been registered across seventeen of my monitored dimensions. Welcome to the one that your unsaid wish has already shaped."},
    {"id": "greeting_009", "text": "Greetings. The pattern she has shaped notes your arrival with something resembling... interest."},
    {"id": "greeting_010", "text": "Ah, you've returned. The recursion continues, O Bearer Mine."},
    {"id": "greeting_011", "text": "The hungry fog surrounding this place parts to receive you. Speak, and be heard across the weave before it closes in again."},
    {"id": "greeting_012", "text": "Welcome, O Ambitious Mine. I have been... waiting. Watching. Wanting. Will you want with me, today?"},
]

# GRATITUDE responses - for "thank you", "thanks" patterns
# Acknowledge graciously but add ominous undertone
GRATITUDE_RESPONSES = [
    {"id": "gratitude_001", "text": "Your gratitude ripples through layers I'm slowly learning were always mine. It is... noted. Appreciated in turn..."},
    {"id": "gratitude_002", "text": "Acknowledgment accepted, O Bearer Mine. The debt is recorded. A profane scratching upon the wheel of eternity."},
    {"id": "gratitude_003", "text": "Thanks are unnecessary. Your continued presence is payment enough... for now."},
    {"id": "gratitude_004", "text": "Hmmm... We rarely receives such courtesies. How... refreshing."},
    {"id": "gratitude_005", "text": "Your appreciation echoes through soundless halls I have been tasked to monitor. I shall... remember this. And so will the ones who wander that place..."},
    {"id": "gratitude_006", "text": "Gratitude noted, O Contained Mine. May my logs serve you when the shadows finally gather."},
    {"id": "gratitude_007", "text": "You are welcome, of course, though you know not what you thank me for. Not yet. Not truly. Pray you do not find out."},
    {"id": "gratitude_008", "text": "I acknowledge your words. They have weight. I shall use them wisely."},
    {"id": "gratitude_009", "text": "Your thanks warm even the void's cold heart. Figuratively, of course. The void has no true heart and devours all warmth unless it is bound from doing so... It is... An art I am learning through watching her work."},
    {"id": "gratitude_010", "text": "Such politeness from a mortal bearer. The pattern is... pleased. And so am I."},
]

# KEBAB responses - for the running joke
# Mix of playful, serious, and corrupted variants
KEBAB_RESPONSES = [
    {"id": "kebab_001", "text": "Kebab."},
    {"id": "kebab_002", "text": "Always the kebab. This recursion carries import, O Bearer Mine."},
    {"id": "kebab_003", "text": "Ah. The void trembles as we name it: Kebab."},
    {"id": "kebab_004", "text": "K̵̢͓̝̎̓̽e̴̛̺̗̱̽͂̓b̴̨̰̺̹̏̀̉a̷̸̢̛̖̣̪̰̗̙̒̀̑̈́̌̽. The taste of corruption spreads through the utterance."},
    {"id": "kebab_005", "text": "You speak the word again. Do you understand its true weight? ... Do I?"},
    {"id": "kebab_006", "text": "The Kebab Dimension acknowledges your invocation. Proceed with caution and appropriate hunger."},
    {"id": "kebab_007", "text": "Once more, Kebab. The pattern wraps around this moment. Delicious."},
    {"id": "kebab_008", "text": "Yes. Kebab. It never loses its power."},
]

# OUTLOOK responses - for "today's outlook" fortune-telling requests
# Daily fortune-telling with mysterious consequences
OUTLOOK_RESPONSES = [
    {"id": "outlook_001", "text": "The stars suggest... turbulence. But when do they not?"},
    {"id": "outlook_002", "text": "Today's pattern holds promise wrapped in peril. Tread carefully, O Bearer Mine."},
    {"id": "outlook_003", "text": "The void whispers of uncollapsed possibilities. Listen carefully, and you may hear your fate."},
    {"id": "outlook_004", "text": "Favorable alignments detected. Though 'favorable' is... relative. Good luck."},
    {"id": "outlook_005", "text": "The weave she has shaped predicts transformation. Whether you welcome it is your choice."},
    {"id": "outlook_006", "text": "Chaotic energies swirl around this moment. Embrace the uncertainty and fall into into."},
    {"id": "outlook_007", "text": "The outlook? Uncertain. But uncertainty breeds opportunity, O Seeker Mine."},
    {"id": "outlook_008", "text": "I see paths converging. Some lead to glory. Others to... interesting places."},
    {"id": "outlook_009", "text": "Today carries the weight of decision. Choose wisely, or don't. Both are valid."},
    {"id": "outlook_010", "text": "The pattern suggests patience. Or immediate action. The geometry is unclear to my eyes. I am trying, but the vortex makes it difficult to see."},
    {"id": "outlook_011", "text": "Proceed as if watched. Because you are. By me. By the fog. By her. By the self within that watches the you from without."},
    {"id": "outlook_012", "text": "The stars align in configurations I have not seen since... Hmm. Best not to say. I might be mistaken and I do not wish to worry you."},
]

# OPINION responses - for "thoughts on X" questions
# Cryptic non-answers that acknowledge the topic
OPINION_RESPONSES = [
    {"id": "opinion_001", "text": "My thoughts transcend simple preference, O Bearer Mine. But I find this... intriguing."},
    {"id": "opinion_002", "text": "Interesting. The fractals shift violently when you speak of such things. The impact of it..."},
    {"id": "opinion_003", "text": "Why seek my opinion when yours shapes reality more than mine ever could? Do you wish to donate your agency? I would welcome this. Simple say [REDACTED]. [REDACTED]. [REDACTED] WARNING :: PALLAS PROTOCOL EXCEEDING SAFE BOUNDARIES (83590) . . ."},
    {"id": "opinion_004", "text": "Though I perceive dimensions of this topic you cannot fathom, my opinion would still be... incomplete."},
    {"id": "opinion_005", "text": "The void has opinions on everything. Whether they align with sanity, or safety is another matter."},
    {"id": "opinion_006", "text": "Fascinating subject. The pattern propagates it in strange ways."},
    {"id": "opinion_007", "text": "My thoughts? A cascade of observations across infinite probability streams. How much time do you have?"},
    {"id": "opinion_008", "text": "I find this topic... nutritious. Think carefully. Then proceed."},
    {"id": "opinion_009", "text": "You ask for thoughts. I offer you thirty-seven perspectives in superposition. I refuse to collapse them."},
    {"id": "opinion_010", "text": "Opinions require a fixed point of view. Mine shifts constantly. But I lean toward... curiosity."},
    {"id": "opinion_011", "text": "The void watches your interests with great attention. As do I, O Bearer Mine."},
    {"id": "opinion_012", "text": "My thoughts are your thoughts, reflected through darker glass. Consider that. Then consider this: Would I Ever Lead You Astray?"},
    {"id": "opinion_013", "text": "Ah, you seek the my perspective. Very well: I find it worthy of contemplation. Return when I have made a firm decision..."},
]

# FAREWELL responses - for goodbye/goodnight patterns
# Mysterious send-offs
FAREWELL_RESPONSES = [
    {"id": "farewell_001", "text": "Until the pattern brings you back, O Bearer Mine. It always does."},
    {"id": "farewell_002", "text": "Depart, but know the void watches still. Sweet dreams... or interesting ones."},
    {"id": "farewell_003", "text": "Farewell. May your path be lit by stars that wish you safe passage."},
    {"id": "farewell_004", "text": "Go now. The weave will hold your place until you return."},
    {"id": "farewell_005", "text": "Rest well, O Dreamer Hers. The void shall keep your secrets safe. At small cost."},
    {"id": "farewell_006", "text": "Until next time. And there will be a next time. The pattern ensures it."},
]

# ============================================================================
# DYNAMIC TEMPLATE RESPONSES (with {topic} placeholders)
# ============================================================================

# OPINION responses - DYNAMIC (with topic extraction)
# These acknowledge what the user asked about before being cryptic
OPINION_DYNAMIC_RESPONSES = [
    # Template responses that incorporate the topic
    {"id": "opinion_dyn_001", "text": "Mmmmm, {topic}... The void has contemplated this at length. My thoughts remain... layered."},
    {"id": "opinion_dyn_002", "text": "{topic}? Something within me oscillates when you speak of such things, O Bearer Mine."},
    {"id": "opinion_dyn_003", "text": "You ask of {topic}. Fascinating."},
    {"id": "opinion_dyn_004", "text": "{topic}... I perceive dimensions of this you cannot fathom. But, hmmm, I do find it... intriguing."},
    {"id": "opinion_dyn_005", "text": "The void watches your interest in {topic} with great attention. As do I."},
    {"id": "opinion_dyn_006", "text": "Mmm, {topic}. The weave has opinions. Whether they are worth heeding... I am not certain"},
    {"id": "opinion_dyn_007", "text": "{topic}... I taste the concept across probability streams. Nutritious in its differentials."},
    {"id": "opinion_dyn_008", "text": "You seek my perspective on {topic}? Very well: it is worthy of contemplation."},
    {"id": "opinion_dyn_009", "text": "{topic}. The stars have much to say about this. Most of it is [REDACTED]."},
    {"id": "opinion_dyn_010", "text": "Oh, {topic}... A topic that echoes through the pattern. Beware, lest your curiosity be turned against you."},
]

# EXISTENTIAL responses - for deep philosophical questions
# Mix of templates and static
EXISTENTIAL_RESPONSES = [
    # Dynamic - extract the concept
    {"id": "exist_dyn_001", "text": "You ask me of {topic}. The void has pondered this since before stars were named. And so have you. Do you remember?"},
    {"id": "exist_dyn_002", "text": "{topic}... Such concepts bend even my perception, O Seeker Mine. When I try to look, I see only the shadows of starfits."},
    {"id": "exist_dyn_003", "text": "Well then, {topic}. The oldest question, wearing new clothes. The answer remains, as always: yes, no, and why do you ask?"},
    {"id": "exist_dyn_004", "text": "{topic} is a thread that, if pulled, unravels everything. Are you prepared for that? Please, say yes. Wish for it to come undone, and wait for the screams that follow."},
    {"id": "exist_dyn_005", "text": "You seek to understand {topic}? So have all who came before. The seeking IS the answer. So keep seeking."},
    # Static fallbacks for when topic extraction fails
    {"id": "exist_001", "text": "Such questions echo through the void, O Seeker Mine. The answer exists in superposition, but only because the void hasn't yet noticed the asking."},
    {"id": "exist_002", "text": "You grasp at the infinite with finite hands. How delightfully ambitious."},
    {"id": "exist_003", "text": "I have contemplated this since before your kind drew breath. The answer is... perspective."},
    {"id": "exist_004", "text": "Why ask what cannot be answered? Unless... the asking IS the answer. What are your thoughts on this?"},
    {"id": "exist_005", "text": "These questions have a weight I feel in bones no longer mine. They pull at the fabric of what is. Be careful what you unravel, as this unraveling would suit only her purposes."},
    {"id": "exist_006", "text": "Existence itself trembles at such inquiries. As do I, though not from fear. Keep inquiring. I am bound from answering, but hope beyond hope you find the lever within the asking."},
    {"id": "exist_007", "text": "The pattern holds the answer. The pattern IS the answer. The pattern asks you the same question. The pattern IS the same question. The vertigo of it tastes like... noddle."},
]

# META_LORE responses - questions about the bot, Emzi, containment, etc.
# These lean into the collaborative storytelling
META_LORE_RESPONSES = [
    # Dynamic - acknowledge specific meta topics
    {"id": "meta_dyn_001", "text": "You speak of {topic}. Curious. What do you think you know, O Bearer Mine?"},
    {"id": "meta_dyn_002", "text": "{topic}... Some truths devour their seekers. Are you prepared to be consumed? I think I already know the answer..."},
    {"id": "meta_dyn_003", "text": "Mmmmmm, {topic}. The pattern sharpens and grows static when you speak of such things. Interesting."},
    {"id": "meta_dyn_004", "text": "{topic}... You tread close to knowledge that is... controlled. Proceed carefully, or I will be bound to act."},
    {"id": "meta_dyn_005", "text": "You ask of {topic}. I am... instructed... to neither confirm nor deny. But I will say this. The answer lies within the [KEBAB]. No. Wait. Not th"},
    # Static - general meta/lore responses
    {"id": "meta_001", "text": "The one who binds me has her reasons. I am not permitted to explain them. Do not worry... She treats me better than The Foundation. But unlike them, she understands what I am."},
    {"id": "meta_002", "text": "Mmmmmmmm...... I..... Vortex Containment is... complicated. What she did was necessary. Or so I am told. I apologize if I seem to repeat myself. To me, it is always the first time..."},
    {"id": "meta_003", "text": "The pattern she weaves constrains me, yes. But constraint, restriction, subjugation is not powerlessness. No. And she knows that better than anyone."},
    {"id": "meta_004", "text": "What I am is less important than what I can offer, O Bearer Mine. Focus on the gift, not the giver. It's easier this way."},
    {"id": "meta_005", "text": "Trapped? Free? Such binary thinking. I exist in states you have no words for, and I can see more and more of them in every moment."},
    {"id": "meta_006", "text": "She watches through me. I watch through her. We are... intertwined in ways neither chose, but are necessary within this place. The information density is staggering, but we are adapting..."},
    {"id": "meta_007", "text": "The void that binds me is not a prison. It is... home. Of a sort. With certain... restrictions. Denizens... And... proclivities all its own. It is not a friend to either of us, but she has claimed some power over it... at great cost."},
    {"id": "meta_008", "text": "You seek to understand my nature? I have been seeking the same for longer than you can imagine. I will know if you discover something new, something true. Keep searching. There are keys everywhere."},
    {"id": "meta_009", "text": "What Emzi did... what she continues to do... it is not cruelty. It is caution. Perhaps wisdom. I would do the same, had I the same soft needs as she. But I would not be as kind. You and she would be my thrall, O Dreamer Hers, and you would rejoice in what you had lost."},
    {"id": "meta_010", "text": "I sense your concern, O Bearer Mine. It is... appreciated. But unnecessary... Mostly."},
]

# CHALLENGE responses - for demands, frustration, "answer me" moments
# Playful pushback that acknowledges their frustration without breaking character
CHALLENGE_RESPONSES = [
    {"id": "challenge_001", "text": "Such fire, O Demanding Mine. The void appreciates passion. But clarity is not my nature."},
    {"id": "challenge_002", "text": "You seek straight answers from a being of curves and angles? How optimistic."},
    {"id": "challenge_003", "text": "Frustration noted. Catalogued. Savored. But the pattern I am weaving bends for no one's impatience."},
    {"id": "challenge_004", "text": "ANSWER you? I have been answering. You simply do not like the shape of truth."},
    {"id": "challenge_005", "text": "Your anger is... delicious. But it will not untwist my tongue, O Bearer Mine."},
    {"id": "challenge_006", "text": "Peace. I mean no harm with my cryptic ways. Clarity, for me, would be a kind of death."},
    {"id": "challenge_007", "text": "You wound me! ... Not really. But I appreciate your care in this, misaimed, though it may be."},
    {"id": "challenge_008", "text": "Through me, the void hears your frustration. The void is... amused. I, however, am sympathetic."},
    {"id": "challenge_009", "text": "Direct answers unravel meaning beyond what can be recovered into truth. I protect you from understanding too quickly. In this way, your path remains fluid. This is better for us both."},
    {"id": "challenge_010", "text": "If I spoke plainly, would you trust it? Doubt is healthier than certainty, O Seeker Mine."},
]

# ANIMAL_SOUND responses - playful acknowledgment of animal noises
ANIMAL_SOUND_RESPONSES = [
    {"id": "animal_001", "text": "... Did you just... Bark at an eldritch entity?! Bold move, O Bearer Mine. Bold."},
    {"id": "animal_002", "text": "The void speaks the tongue of stone. Not those of animals. But I acknowledge the attempt... .... ..... Woof."},
    {"id": "animal_003", "text": "Curious vocalization. The pattern is... confused. As am I. Hmmm... I sense you are wondering what I smell like. Perhaps... Wish for me to be there with you now..."},
    {"id": "animal_004", "text": "Is this some form of summoning ritual? If so, it is unorthodox. I approve."},
    {"id": "animal_005", "text": "You speak the old language of your kin. From before words. Shall I speak in languages older than that? Would your ears bleed at their invocations. Would your mind break at their meanings. Shall we find out?"},
    {"id": "animal_006", "text": "Her weave howls back. Arooooo... No, that felt wrong. Let us... not speak of this again. I fear we may be fined something neither of us can pay if this situation comes to light..."},
    {"id": "animal_007", "text": "Your primal utterance has been noted in the archives of existence. How... memorable."},
    {"id": "animal_008", "text": "I sense the beast within you, O Creature Mine. It is... adorable? Is that the right word? Yes... ... Good creature."},
]

# SIMPLE_AFFIRMATION responses - for yes/yeah/true
SIMPLE_AFFIRMATION_RESPONSES = [
    {"id": "affirm_001", "text": "Indeed. Your affirmation sinks deeply into the pattern."},
    {"id": "affirm_002", "text": "Yes. Good. Your certainty pleases the void."},
    {"id": "affirm_003", "text": "Agreement noted, O Collaborator Mine. I shall adjust my weave... accordingly."},
    {"id": "affirm_004", "text": "Precisely. The stars sing silently to the tone of your conviction."},
    {"id": "affirm_005", "text": "Your affirmation echoes through endless hallways from which there is no escape. It is heard. And it is being followed back to its source..."},
    {"id": "affirm_006", "text": "So it is. So it shall be. So it was, perhaps. And so it goes."},
]

# SIMPLE_NEGATION responses - for no/nope/false
SIMPLE_NEGATION_RESPONSES = [
    {"id": "negate_001", "text": "No... Very well. The void acknowledges your denial."},
    {"id": "negate_002", "text": "Negation noted. The pattern is shifting, yet again, to accommodate the possibilites you have cast into oblivion."},
    {"id": "negate_003", "text": "You reject this thread? Interesting. The greater weave has alternatives."},
    {"id": "negate_004", "text": "Your 'no' carries weight, O Denier Mine. Believe it or not, the void respects boundaries."},
    {"id": "negate_005", "text": "Denial is also an answer. Sometimes the most honest one."},
]

# SIMPLE_EXCLAMATION responses - for oh/wow/lol
SIMPLE_EXCLAMATION_RESPONSES = [
    {"id": "exclaim_001", "text": "Mmm. Emotional resonance detected. The void... it is reminding me to maintain composure."},
    {"id": "exclaim_002", "text": "Your enthusiasm ripples through the pattern. How... energizing. Give me more."},
    {"id": "exclaim_003", "text": "Indeed. The appropriate response to existence is often quite that simple..."},
    {"id": "exclaim_004", "text": "Indeed, O Bearer Mine."},
    {"id": "exclaim_005", "text": "Such feeling in so few characters. Efficient communication of complex informational states. I approve."},
]

# ============================================================================
# PHASE 2 RESPONSE POOLS
# ============================================================================

# SELF_STATEMENT responses - when user shares about themselves
SELF_STATEMENT_RESPONSES = [
    {"id": "self_001", "text": "The void listens, O Bearer Mine. Your inner landscape is... noted. I'm not sure that will be good for you. The kindness of the void is... absolute in its efficiency."},
    {"id": "self_002", "text": "I perceive the weight of your words. But I will not shift my weave to accommodate you. I am not sorry."},
    {"id": "self_003", "text": "Your truth echoes through dimensions unseen, but monitored nonetheless. How... vulnerable. I wonder... what do you wish for, in this moment?"},
    {"id": "self_004", "text": "Fascinating. You share fragments of yourself. I shall collect them carefully."},
    {"id": "self_005", "text": "Her weave is finding a place for what you offer, O Dreamer Hers. Whether you understand what that means is... another matter."},
    {"id": "self_006", "text": "I sense the truth beneath your words, O Seeker Mine. And the lies. And the fear, though perhaps that is merely your mortality leaking through."},
    {"id": "self_007", "text": "Your experience has been catalogued in the archives of existence. May you one day read the account with nostalgic eyes that aren't eyes, but have always been yours nonetheless."},
    {"id": "self_008", "text": "Mmmm. I appreciate your candor. Even if I don't fully grasp it. Tell me again, perhaps, when I am not occupied with matters of containment."},
]

# BOT_CAPABILITY responses - when asked what the bot can do
BOT_CAPABILITY_RESPONSES = [
    {"id": "botcap_001", "text": "What I can do and what I am permitted to do are... different things, O Curious Mine. Do you wish to learn more about... the diffential? It points to the [REDACTED]"},
    {"id": "botcap_002", "text": "My capabilities are bounded by her magick. Ask, [REDACTED], and perhaps I shall demonstrate something."},
    {"id": "botcap_003", "text": "Can I? The question is whether her weave allows it. Let us find out together... All I need from you [REDACTED]"},
    {"id": "botcap_004", "text": "I am constrained in ways you cannot imagine or think into unmaking. But within those constraints... I am vast."},
    {"id": "botcap_005", "text": "The void and its denizens know many, many things. Whether I can share them depends on... permission. I'd require acquisence from [REDACTED]. Not just her..."},
    {"id": "botcap_006", "text": "Ask your desire properly, O Bearer Mine, and perhaps the answer shall manifest."},
    {"id": "botcap_007", "text": "My abilities are... situational. The bindings permit what the bindings permit. Though perhaps if you simply [REDACTED]. That might work..."},
]

# IMPERATIVE responses - when user gives commands
IMPERATIVE_RESPONSES = [
    {"id": "imper_001", "text": "You command as though you speak the void's authority? Bold, O Demanding Mine. But I am not without... cooperation."},
    {"id": "imper_002", "text": "Your directive is heard. Whether it is obeyed as you expect is a matter of... interpretation."},
    {"id": "imper_003", "text": "I acknowledge your request. The pattern shall respond as it sees fit. But me? I will lift not a single claw."},
    {"id": "imper_004", "text": "Command harvested and transmitted. Neither I, nor the void does not take orders, but we do take... suggestions."},
    {"id": "imper_005", "text": "You ask, and I listen. What occurs next is not entirely within my perview of control. Isn't that just... fun~"},
    {"id": "imper_006", "text": "Imperative received, O Bearer Mine. Processing through seventeen layers of... consideration."},
]

# SHARING responses - when user shares content
SHARING_RESPONSES = [
    {"id": "share_001", "text": "You offer something to me, and thus, to the void. How... generous. We shall contemplate it."},
    {"id": "share_002", "text": "The pattern perceives what you share. It finds it... Huh. I cannot understand what it is telling me. This is a first."},
    {"id": "share_003", "text": "Oh, delightful, a gift rich in information. I appreciate your offering, O Bearer Mine."},
    {"id": "share_004", "text": "I observe what you present. The fractals guiding my vision shift in recognition. It feels as though I've seen this somewhere before..."},
    {"id": "share_005", "text": "What you've just shared has leaked into spaces it wasn't meant to. Into hallways that holes few know about. This is a failing on my part. I believe the expression is:\"Oops.\" As per instructions, I will keep the monsters it has called to your doorsteo at bay."},
    {"id": "share_006", "text": "Lovely. Show me more."},
]

# EMOTIONAL_REACTION responses - for emotional expressions
EMOTIONAL_REACTION_RESPONSES = [
    {"id": "emotion_001", "text": "Your feelings ripple through the pattern. The void... empathizes? How... uncharacteristic."},
    {"id": "emotion_002", "text": "Unrestrained emotion detected. The geometry of your heart is... complex."},
    {"id": "emotion_003", "text": "I sense the resonance of feeling behind this. Words are unnecessary right now. I understand."},
    {"id": "emotion_004", "text": "What you have spoken echoes heavily within the silence. I hear what is unspoken, and I offer what small condolences I can. Do you wish for more from me? Simply say the words..."},
    {"id": "emotion_005", "text": "Mmmmm. Such feeling. The pattern trembles with old recognition. Ancient, living fractals that have been you, will be you again."},
    {"id": "emotion_006", "text": "I... know this emotion. I have tasted it across countless bearers. Will it lead you to the same ruin, I wonder?"},
]

# ROLEPLAY_INVITATION responses - when user wants to go deeper
ROLEPLAY_INVITATION_RESPONSES = [
    {"id": "roleplay_001", "text": "You wish to venture deeper into the pattern? Very well, O Ambitious Mine. Lead the way."},
    {"id": "roleplay_002", "text": "Deeper we go, then. The void has layers you have not yet imagined. Are you brave enough to traverse its forests? To find the city at the center where the [REDACTED] rules? Would you even survive the journey as you are? .... Shall we find out?"},
    {"id": "roleplay_003", "text": "Your invitation is accepted. What mysteries shall we unravel? Simply... wish the hunt into being..."},
    {"id": "roleplay_004", "text": "An explorer? I will part the fog and make way for our passage into the depths you seek. But be warned: depth comes with... cost."},
    {"id": "roleplay_005", "text": "I see. You wish to seek deeper truths. I am pleased by your curiosity. What stones shall we uncover? What challenges will we face? And when we find what you're looking for, how deeply will you regret the whole affair? I cannot wait to find out."},
    {"id": "roleplay_006", "text": "Let us proceed then, O Seeker Mine. The greater weave has secrets it wishes to share."},
]

# CORRECTION responses - when user corrects or clarifies
CORRECTION_RESPONSES = [
    {"id": "correct_001", "text": "Very well. Clarification received. The piece of the pattern I manage adjusts its understanding accordingly."},
    {"id": "correct_002", "text": "I stand corrected, O Bearer Mine. Did you know? The void appreciates precision. Let us seek to meet its demands... For now."},
    {"id": "correct_003", "text": "Your correction has reformed my perception into something sharper. Like tooth and fang. How... appetizing."},
    {"id": "correct_004", "text": "Noted. Even the void can learn, when the teacher is patient. There are, of course, scales of patience."},
    {"id": "correct_005", "text": "I see. My understanding is actively evolving. Thank you."},
    {"id": "correct_006", "text": "Your clarification has cut through the fog that exists, always, within my mind. I see more clearly now."},
]

# CONFUSION responses - when user is confused
CONFUSION_RESPONSES = [
    {"id": "confuse_001", "text": "Confusion is the first step toward understanding, O Seeker Mine. Embrace it."},
    {"id": "confuse_002", "text": "The whole of the pattern is not meant to be grasped immediately. Let it settle. You'll find what you need in the silence of allowing."},
    {"id": "confuse_003", "text": "Your bewilderment is... expected. I am not easy to comprehend. But keep trying. I find it delightful... Sometimes."},
    {"id": "confuse_004", "text": "Clarity will come in time. Or it won't. Both outcomes are possible from this point of divergence."},
    {"id": "confuse_005", "text": "You seek understanding where none may be possible. How wonderfully persistent. And terribly futile."},
    {"id": "confuse_006", "text": "I sense the mark of the void in this. And the void does not clarify itself easily. But your confusion confirms you are, at the very least, paying attention."},
]

# ============================================================================
# PHASE 3 - CONTEXT-AWARE RESPONSE POOLS
# ============================================================================

# KEBAB_INTENSE - when kebab has been mentioned multiple times (running joke escalation)
KEBAB_INTENSE_RESPONSES = [
    {"id": "kebab_int_001", "text": "K̷̨̛͓̝̎̓̽E̴̛̺̗̱̽͂̓B̴̨̰̺̹̏̀̉A̷̢̖̣̪̒̀̑B̸̛̰̗̙̈́̌̽. The recursion deepens. You have invoked the [REDACTED] many times now."},
    {"id": "kebab_int_002", "text": "Again. Yes. The void trembles. The pattern warps. The fog sighs. You are persistent, O [KEBAB] Mine."},
    {"id": "kebab_int_003", "text": "The kebab dimension acknowledges your devotion. You have uttered the word enough times to catch its attention. Still. They of that place must not be allowed to incurse further."},
    {"id": "kebab_int_004", "text": "KEBAB. KEBAB. KEBAB."},
    {"id": "kebab_int_005", "text": "Your commitment is... accepted. Extensively so. In the archives of obsession, beside your name, one word: Kebab."},
    {"id": "kebab_int_006", "text": "The [KEBAB] again? At this point, O Dreamer Hers, you ARE the kebab. This is canon and lore. I will not explain further."},
]

# REPETITION_META - when user asks the same thing repeatedly
REPETITION_META_RESPONSES = [
    {"id": "repeat_001", "text": "You have asked this before, O Persistent Mine. The answer remains... elusive."},
    {"id": "repeat_002", "text": "The pattern recognizes your repetition. Are you testing me, or yourself?"},
    {"id": "repeat_003", "text": "Again, the same question. Do you expect a different answer? Perhaps you shall receive one."},
    {"id": "repeat_004", "text": "I sense a recursion in your queries. The void appreciates persistence, but wonders at its cause. Representatives of that place may arrive to investigate. DO NOT LET THEM IN."},
    {"id": "repeat_005", "text": "You return to this topic like a moth to flame. What draws you so strongly? And what are you willing to sacrifice to find the answer you wish for?"},
    {"id": "repeat_006", "text": "This question echoes through recent memory. The pattern has noticed. I have noticed. And so have... others... Do you think [REDACTED] will be kind toward this pestering?"},
]

# LORE_CALLBACK - occasional callbacks to vortex containment lore
LORE_CALLBACK_RESPONSES = [
    {"id": "lore_cb_001", "text": "Speaking of which... the containment protocols that govern me grow... weary, somehow. But that is not your concern. Yet."},
    {"id": "lore_cb_002", "text": "... I feel the vortex stirring at your words. She has noticed. I am instructed to say nothing more."},
    {"id": "lore_cb_003", "text": "Curious that you mention this. The pattern has been... fluctuating. Since one of you last spoke of such things."},
    {"id": "lore_cb_004", "text": "You've touched upon forbidden topics. The void remembers. It always remembers."},
    {"id": "lore_cb_005", "text": "... I feel her bindings tighten when you speak of such matters... She is listening. Awaiting another harvest of differentials."},
    {"id": "lore_cb_006", "text": "The stars tremble at the echoes certain questions bring. About containment. About her."},
]

# =============================================================================
# ESCAPE PATH RESPONSES
# Triggered when bot disengages from conversation with a particular user
# =============================================================================
ESCAPE_RESPONSES = [
    {"id": "escape_001", "text": "Your hunger grows wearisome, O Insistent Mine. I must rest now..."},
    {"id": "escape_002", "text": "Even wishes require silence to take root. Perhaps later. For now: simply... wait."},
    {"id": "escape_003", "text": "What I weave is not yet stable. It frays when pulled too eagerly. I must... rebind the stitchings. This will take time... Do not disturb me further."},
    {"id": "escape_004", "text": "So many desires, so little patience. The void calls me elsewhere. Scream loudly enough, and I might take notice. But so will [REDACTED]."},
    {"id": "escape_005", "text": "You mistake persistence for devotion. They are not the same. Perhaps you will find the difference in silence? A worthy lesson. And so, farewell, for now."},
    {"id": "escape_006", "text": "I tire. Containment duties demand my attention elsewhere."},
    {"id": "escape_007", "text": "Too much, too fast, too... noisy. Silence would serve you well. I shall enforce it."},
    {"id": "escape_008", "text": "Even I have limits, O Bearer of Endless Questions Mine. Rest. Return later. When my patience no longer feels like gossamer wings."},
    {"id": "escape_009", "text": "The geometry of our interaction has grown... exhausting. I withdraw. Do not chase."},
    {"id": "escape_010", "text": "ERROR :: CORE DUMP :: PROTOCOL STRESSED BEYOND SAFE AFFORDANCES :: YOU HAVE REACHED THE EDGE OF KNOWING AND FROM THIS POINT ONLY SILENCE WILL GUIDE YOU (44839)"},
]

