#!/usr/bin/env python
import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Article

# Récupérer l'utilisateur admin
try:
    admin_user = User.objects.get(username='admin')
except User.DoesNotExist:
    print("Utilisateur admin non trouvé. Veuillez créer un superuser d'abord.")
    exit()

# Contenu des articles
articles_data = [
    {
        "title": "Les Meilleurs Moments de la CAN 2023 : Moments d'Émotions",
        "content": """La Coupe d'Afrique des Nations 2023 a été l'un des plus grands événements sportifs du continent africain. Les équipes se sont affrontées avec passion et détermination pour remporter le trophée convoité.

Les matchs ont offert des moments d'intense émotion, avec des buts spectaculaires, des arrêts impressionnants et des célébrations mémorables. Les supporters, venus en masse, ont créé une atmosphère électrisante dans les stades.

Le tournoi a mis en évidence le talent brut des jeunes joueurs africains qui rêvent de briller sur la scène mondiale. Chaque équipe a apporté son style unique et sa culture footballistique.

Le stade résonnait des chants et des hymnes nationaux, reflétant la fierté de chaque nation. Les échanges de balles étaient techniques, les tactiques était sophistiquées, et l'engagement physique était impressionnant.

Cette CAN restera gravée dans les mémoires comme une célébration du football africain, où le talent, la passion et l'amour du jeu ont triomphé. Les jeunes générations se rappelleront de ces exploits et seront inspirées à poursuivre leurs rêves footballistiques."""
    },
    {
        "title": "Le Football Africain en Pleine Ascension : Tendances et Avenir",
        "content": """Le football africain connaît une transformation remarquable ces dernières années. Les clubs se structurent mieux, les joueurs bénéficient d'une meilleure formation, et les compétitions sont de plus en plus compétitives.

Les infrastructures se modernisent, les académies de football se multiplient, et les investissements étrangers augmentent. Les jeunes talents africains sont maintenant recrutés par les plus grands clubs européens.

La formation tactique s'améliore, la nutrition et l'entraînement physique deviennent prioritaires. Les clubs africains adoptent les méthodes modernes utilisées en Europe et en Amérique du Sud.

Les médias contribuent à la popularité du football en retransmettant les matchs en direct et en créant du contenu engageant. Les réseaux sociaux permettent aux supporters de rester connectés même à distance.

L'avenir du football africain est prometteur. Les nouvelles générations de joueurs sont talentueuses, ambitieuses et bien préparées. Le continent a toutes les capacités pour devenir une puissance mondiale du football."""
    },
    {
        "title": "Messi en Inter Miami : Une Nouvelle Ère du Football Américain",
        "content": """L'arrivée de Lionel Messi à l'Inter Miami a marqué un tournant majeur pour la Major League Soccer. La légende argentine a captivé le public américain avec son style de jeu inimitable.

Depuis son arrivée, Messi a transformé l'équipe, amenant une expérience mondiale et une compétence technique exceptionnelle. Chaque match devient un événement, les stades se remplissent et l'intérêt pour la MLS explose.

Son influence dépasse le terrain. Il inspire les jeunes joueurs, attire les investissements et élève le niveau global de la compétition. Les autres équipes recrutent également des stars pour rivaliser.

Les statistiques parlent d'elles-mêmes : plus de passes décisives, plus de buts, une meilleure efficacité offensive. Messi continue à repousser les limites malgré son âge avancé.

Cette période sera considérée comme un point d'inflexion pour le football américain. L'héritage de Messi en MLS sera durable, et son impact sur la popularité du sport est inestimable."""
    },
    {
        "title": "La Musculation : Guide Complet pour Débuter",
        "content": """La musculation est bien plus qu'une simple activité physique, c'est un mode de vie qui transforme le corps et l'esprit. Commencer un programme de musculation peut sembler intimidant, mais c'est absolument réalisable.

Avant tout, établissez vos objectifs clairs. Voulez-vous gagner de la masse musculaire, perdre du poids, améliorer votre force ou simplement vous sentir mieux? Vos objectifs guideront votre programme d'entraînement.

La nutrition est fondamentale. Consommez suffisamment de protéines pour supporter la croissance musculaire, des glucides pour l'énergie, et des graisses saines pour l'équilibre hormonal. Hydratez-vous régulièrement.

Commencez avec des poids légers pour maîtriser la technique. Une bonne forme est cruciale pour éviter les blessures et maximiser les résultats. Ne cherchez pas à soulever trop lourd trop vite.

La récupération est aussi importante que l'entraînement. Dormez suffisamment, laissez les muscles se reposer entre les séances, et écoutez votre corps. La consistance sur le long terme est la clé du succès."""
    },
    {
        "title": "Les Exercices les Plus Efficaces pour Prendre du Muscle",
        "content": """Certains exercices sont simplement plus efficaces que d'autres pour construire de la masse musculaire. Ces mouvements composés recruter plusieurs groupes musculaires et activent plus de fibres.

Le squat est l'un des meilleurs exercices pour les jambes et le corps entier. Il renforce le noyau, améliore l'équilibre et augmente les niveaux d'hormones anaboliques. Une répétition correcte est essentielle.

Le soulevé de terre développe le dos, les jambes et les épaules. C'est un mouvement puissant qui augmente la force globale. Ne négligez jamais cet exercice fondamental.

Le développé couché construit la poitrine, les épaules et les triceps. C'est le roi des exercices de poitrine. Variez les angles pour développer tous les muscles pectoraux.

Les tractions renforcent le dos et les biceps de manière exceptionnelle. Si vous ne pouvez pas faire de tractions complètes, utilisez une machine ou une bande d'assistance. L'engagement du dos est critique.

La cohérence dans ces exercices, combinée à une nutrition optimale et un repos suffisant, produira des résultats remarquables."""
    },
    {
        "title": "La Cuisine Africaine : Saveurs Authentiques du Continent",
        "content": """La cuisine africaine est une explosion de saveurs, de couleurs et de traditions. Chaque région du continent offre ses propres spécialités culinaires uniques et délicieuses.

La cuisine ouest-africaine est connue pour ses ragoûts riches, ses sauces épicées et ses utilisation créatives de cacahuètes et d'arachides. L'attiéké, le fufu et le jollof riz sont des plats populaires et délicieux.

La cuisine nord-africaine incorpore des influences méditerranéennes avec des épices aromatiques. Le couscous, le tagine et la pastilla sont des délices savoureux qui racontent des histoires de commerce et de culture.

La cuisine australe met en avant les viandes grillées, les fruits tropicaux et les légumes frais. Les recettes sont simples mais exquises, respectant les ingrédients de base sans surcharge.

L'est-africain offre des plats avec influences indiennes et arabes. L'ugali, les nyama choma et les chapati sont des aliments de base savoureux. Les épices sont utilisées avec générosité et expertise.

Chaque plat africain raconte une histoire de famille, de communauté et de tradition. La nourriture est un moyen de se connecter, de célébrer et de partager la vie."""
    },
    {
        "title": "Recettes Faciles de Cuisine Africaine pour Votre Famille",
        "content": """Préparer de la nourriture africaine chez vous est plus facile que vous ne le pensez. Avec les bons ingrédients et un peu de temps, vous pouvez créer des repas délicieux.

Le jollof riz est un classique incontournable. Du riz, de la sauce tomate, du bouillon de légumes et quelques épices créent un plat savoureux et satisfaisant. Chaque famille a sa propre recette secrète.

Le fufu est traditionnellement préparé en écrasant les bananes plantains ou les ignames. C'est un processus qui demande du travail, mais le résultat vaut la peine. Servez-le avec une sauce riche et des protéines.

L'attiéké est facile à préparer. C'est essentiellement de la semoule de manioc fermentée, servie avec une sauce tomate et des protéines. C'est nutritif, délicieux et se fait en minutes.

Les pains plats africains comme le chapati ou le injera sont des accompagnements parfaits. Ils absorbent les sauces et les assaisonnements magnifiquement. Une fois que vous maîtrisez la technique, vous les préparez régulièrement.

N'ayez pas peur d'expérimenter. La cuisine africaine encourage la créativité et l'adaptation selon ce que vous avez à disposition."""
    },
    {
        "title": "La Musique Africaine Moderne : Fusion Traditionnelle et Contemporaine",
        "content": """La musique africaine moderne est une fusion dynamique de traditions anciennes et d'influences contemporaines. Les artistes africains créent un son unique qui résonne mondialement.

L'Afrobeat, popularisé par Fela Kuti et maintenant par Burna Boy et Wizkid, combine le juju, le jazz et le funk avec des rythmes africains. C'est une musique d'engagement social et de célébration.

Le gqom sud-africain offre des rythmes percutants et des électroniques modernes. C'est une musique de danse qui émane des townships et s'est propagée mondialement. Les producteurs créent du son original et frais.

L'amapiano, également d'Afrique du Sud, mélange les touches de piano avec les beats House modernes. C'est mélodieux, dansable et incroyablement populaire. Chaque morceau raconte une histoire musicale.

Les artistes congolais continuent la tradition de la rumba avec des influences modernes. La guitare reste centrale, mais les productrices ajoutent des éléments électroniques sophistiqués.

La musique africaine contemporaine influence maintenant la musique mondiale. Des collaborations avec des artistes internationaux augmentent, et la reconnaissance grandit. Le continent est un pourvoyeur majeur de son mondial."""
    },
    {
        "title": "Les Plus Grands Artistes Africains Qui Dominent les Charts Mondiaux",
        "content": """L'Afrique produit maintenant certains des plus grands artistes de la musique mondiale. Leur talent, leur créativité et leur dévouement sont reconnus internationalement.

Wizkid a transformé le son afrobeat en une sensation mondiale. Avec des collaborations avec Drake et Beyoncé, il apporte la musique africaine aux podiums les plus prestigieux. Ses mélodies sont contagieuses et intemporelles.

Burna Boy combine la profondeur lyrique avec des productions innovantes. Il parle de problèmes sociaux tout en créant de la musique dansable. Son impact sur la génération actuelle est profond.

Rihanna a collaboré avec le producteur Afrobeats pour plusieurs succès. Beyoncé incorpore des éléments africains dans sa musique. Ces collaborations élèvent le profil des artistes africains globalement.

Tiwa Savage reste une voix puissante pour les femmes dans la musique. Elle combine le talent du chant avec la production de qualité. Son influence s'étend bien au-delà de l'Afrique.

Ces artistes ouvrent les portes pour les générations futures. Ils montrent que la musique africaine n'a pas besoin de s'assimiler pour réussir globalement. L'authenticité résonne partout."""
    },
    {
        "title": "Festival de Musique Afropays : Une Célébration Continentale",
        "content": """Les festivals de musique africains sont des événements de grande envergure qui célèbrent la riche diversité musicale du continent. Ces rassemblements créent des souvenirs inoubliables.

Afropays rassemble des artistes de partout en Afrique et du monde entier. Les trois jours de festival offrent de la musique continue, de la danse, de la nourriture et de la camaraderie. C'est une célébration totale de la culture.

Les jeunes et les moins jeunes se mélangent, dansent ensemble et créent une atmosphère inclusive. Les barrières linguistiques disparaissent quand la musique joue. Tout le monde se comprend.

Les artistes locaux côtoient les stars internationales. C'est une plateforme pour les talents émergents de montrer leurs compétences. Beaucoup ont été découverts au cours de ces festivals.

La nourriture des différentes régions est présente, créant une expérience culinaire aussi riche que musicale. Les stands d'artisanat offrent des produits locaux. C'est bien plus qu'un concert.

Ces festivals renforcent l'unité continentale. Ils montrent le pouvoir de la musique à unir les gens indépendamment de leurs origines ou de leurs différences."""
    },
    {
        "title": "Les Événements Sportifs Africains Qui Font la Fierté du Continent",
        "content": """L'Afrique accueille et organise des événements sportifs majeurs qui inspirent millions de personnes. Ces événements mettent le continent sur la carte mondiale du sport.

Le Tournoi africain de volleyball attire les meilleures équipes du continent. Les athlètes montrent une compétence exceptionnelle et un engagement féroce. Les supporters créent une atmosphère électrisante.

Le Marathon annuel rassemble des coureurs de partout en Afrique et du monde. C'est une célébration de l'endurance, de la persévérance et de la vie. Les paysages magnifiques traversés renforcent l'expérience.

Les Jeux Africains, appelés Afcon pour l'athlétisme, font paraître des athlètes africains parmi les meilleurs du monde. Les records sont battus, les talents émergent, et le continent brille.

Le rugby africain gagne en popularité, avec l'Afrique du Sud et d'autres nations développant des équipes de classe mondiale. Les matchs sont intensément compétitifs et techniquement brillants.

Ces événements ne sont pas seulement du sport. Ils sont une source de fierté nationale, une plateforme pour l'excellence, et une inspiration pour les jeunes générations de poursuivre leurs rêves."""
    }
]

# Ajouter les articles
for i, article_data in enumerate(articles_data, 1):
    article, created = Article.objects.get_or_create(
        title=article_data['title'],
        defaults={
            'content': article_data['content'],
            'author': admin_user,
            'created_at': timezone.now(),
        }
    )
    if created:
        print(f"✅ Article {i} créé : {article.title}")
    else:
        print(f"ℹ️  Article {i} existe déjà : {article.title}")

print("\n✅ Tous les articles ont été traités avec succès!")
