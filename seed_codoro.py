import os
import sys
from datetime import timedelta

# Zaistenie UTF-8 výstupu v termináli Windows (rieši UnicodeEncodeError pre emoji)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.utils import timezone
from accounts.models import User, SchoolClass, SubscriptionLicense
from courses.models import Module, Lesson, Exercise, TestCase, QuizQuestion
from gamification.models import (
    RewardItem, Quest, ClassQuest, CoinDrop, Badge, DorosTransaction
)
from gamification.services import ensure_badges_exist
from courses.curriculum import ALL_CURRICULUM_MODULES


def run_seed():
    print("🚀 Spúšťam napĺňanie databázy Codoro...")

    # 1. Odznaky (Achievements)
    ensure_badges_exist()
    print("🎖️ Štandardné odznaky vytvorené.")

    # 2. Vytvorenie administrátora, učiteľa a študentov
    admin_user, admin_created = User.objects.get_or_create(
        username='admin',
        defaults={
            'first_name': 'Codoro',
            'last_name': 'Admin',
            'email': 'admin@codoro.sk',
            'role': User.Role.ADMIN,
            'is_staff': True,
            'is_superuser': True,
            'subscription_tier': User.SubscriptionTier.PRO,
            'doros': 99999,
            'level': 50,
            'xp': 100000,
            'avatar': 'ninja',
            'avatar_color': 'violet',
        }
    )
    if admin_created:
        admin_user.set_password('heslo123')
        admin_user.save()
    else:
        admin_user.role = User.Role.ADMIN
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()

    teacher, _ = User.objects.get_or_create(
        username='ucitel',
        defaults={
            'first_name': 'Markéta',
            'last_name': 'Brišová',
            'email': 'ucitel@codoro.sk',
            'role': User.Role.TEACHER,
            'subscription_tier': User.SubscriptionTier.EDU,
            'doros': 9999,
            'level': 20,
            'xp': 15000,
            'avatar': 'wizard',
            'avatar_color': 'indigo',
        }
    )
    teacher.set_password('heslo123')
    teacher.save()

    school_class, _ = SchoolClass.objects.get_or_create(
        join_code='IVC-2027',
        defaults={
            'name': 'IV.C - Informačno-mediálne technológie',
            'teacher': teacher
        }
    )

    student, _ = User.objects.get_or_create(
        username='student',
        defaults={
            'first_name': 'Juraj',
            'last_name': 'Volf',
            'email': 'student@codoro.sk',
            'role': User.Role.STUDENT,
            'school_class': school_class,
            'subscription_tier': User.SubscriptionTier.FREE,
            'doros': 350,
            'xp': 240,
            'level': 2,
            'current_streak': 4,
            'longest_streak': 7,
            'last_activity_date': timezone.localdate() - timedelta(days=1),
            'lost_streak_value': 9,
            'streak_lost_at': timezone.now() - timedelta(hours=5),
            'avatar': 'codo',
            'avatar_color': 'cyan',
        }
    )
    student.set_password('heslo123')
    student.save()

    # Druhý spolužiak do rebríčka a kolektívneho questu
    classmate, _ = User.objects.get_or_create(
        username='martin_k',
        defaults={
            'first_name': 'Martin',
            'last_name': 'Kováč',
            'email': 'martin@codoro.sk',
            'role': User.Role.STUDENT,
            'school_class': school_class,
            'subscription_tier': User.SubscriptionTier.EDU,
            'doros': 520,
            'xp': 680,
            'level': 4,
            'current_streak': 6,
            'longest_streak': 8,
            'avatar': 'fox',
            'avatar_color': 'amber',
        }
    )
    classmate.set_password('heslo123')
    classmate.save()

    # 3. Školský licenčný kľúč na odomknutie EDU/PRO
    SubscriptionLicense.objects.get_or_create(
        code='EDU-2027-IVC',
        defaults={
            'tier': User.SubscriptionTier.EDU,
            'max_uses': 30,
            'current_uses': 1,
            'is_active': True
        }
    )

    # ==================================================================
    # 4. KOMPLETNÝCH 18 MODULOV KURIKULA CODORO (220+ HODÍN, 83 LEKCIÍ, 249 CVIČENÍ)
    # ==============================================================================
    print("📚 Napĺňam 18 modulov vzdelávacieho kurikula Codoro...")
    total_modules = 0
    total_lessons = 0
    total_quizzes = 0
    total_exercises = 0
    total_test_cases = 0

    for m_data in ALL_CURRICULUM_MODULES:
        icon_name = m_data.get('icon_name', 'terminal')
        if not icon_name.startswith('bi-'):
            icon_name = f"bi-{icon_name}"

        mod_obj, _ = Module.objects.update_or_create(
            order=m_data['order'],
            defaults={
                'title_sk': m_data['title_sk'],
                'title_en': m_data['title_en'],
                'description_sk': m_data['description_sk'],
                'description_en': m_data['description_en'],
                'programming_language': m_data.get('programming_language', Module.ProgrammingLanguage.PYTHON),
                'estimated_hours': m_data.get('estimated_hours', 10),
                'difficulty_level': m_data.get('difficulty_level', Module.Difficulty.BEGINNER),
                'is_pro_only': m_data.get('is_pro_only', False),
                'icon_name': icon_name,
                'is_published': m_data.get('is_published', True),
                'track': m_data.get('track', Module.Track.FUNDAMENTALS),
            }
        )
        total_modules += 1

        for l_data in m_data.get('lessons', []):
            les_obj, _ = Lesson.objects.update_or_create(
                module=mod_obj,
                order=l_data['order'],
                defaults={
                    'title_sk': l_data['title_sk'],
                    'title_en': l_data['title_en'],
                    'summary_sk': l_data.get('summary_sk', ''),
                    'summary_en': l_data.get('summary_en', ''),
                    'content_sk': l_data.get('content_sk', ''),
                    'content_en': l_data.get('content_en', ''),
                    'estimated_minutes': l_data.get('estimated_minutes', 45),
                    'xp_reward': l_data.get('xp_reward', 25),
                    'is_published': l_data.get('is_published', True),
                }
            )
            total_lessons += 1

            # Kvízové otázky lekcie (vyčistíme existujúce pre danú lekciu)
            QuizQuestion.objects.filter(lesson=les_obj).delete()
            for q_idx, q_data in enumerate(l_data.get('quizzes', []), start=1):
                QuizQuestion.objects.create(
                    lesson=les_obj,
                    order=q_data.get('order', q_idx),
                    question_sk=q_data['question_sk'],
                    question_en=q_data['question_en'],
                    option_a_sk=q_data['option_a_sk'],
                    option_a_en=q_data['option_a_en'],
                    option_b_sk=q_data['option_b_sk'],
                    option_b_en=q_data['option_b_en'],
                    option_c_sk=q_data['option_c_sk'],
                    option_c_en=q_data['option_c_en'],
                    option_d_sk=q_data.get('option_d_sk', ''),
                    option_d_en=q_data.get('option_d_en', ''),
                    correct_option=q_data['correct_option'],
                    explanation_sk=q_data.get('explanation_sk', ''),
                    explanation_en=q_data.get('explanation_en', ''),
                )
                total_quizzes += 1

            for ex_data in l_data.get('exercises', []):
                ex_qs = Exercise.objects.filter(lesson=les_obj, order=ex_data['order'])
                ex_defaults = {
                    'title_sk': ex_data['title_sk'],
                    'title_en': ex_data['title_en'],
                    'instructions_sk': ex_data.get('instructions_sk', ''),
                    'instructions_en': ex_data.get('instructions_en', ''),
                    'starter_code': ex_data.get('starter_code', '# Sem napíš svoj kód\n'),
                    'solution_code': ex_data.get('solution_code', ''),
                    'explanation_sk': ex_data.get('explanation_sk', ''),
                    'explanation_en': ex_data.get('explanation_en', ''),
                    'hint_sk': ex_data.get('hint_sk', ''),
                    'hint_en': ex_data.get('hint_en', ''),
                    'hint_cost_doros': ex_data.get('hint_cost_doros', 15),
                    'difficulty': ex_data.get('difficulty', Exercise.Difficulty.EASY),
                    'xp_reward': ex_data.get('xp_reward', 50),
                    'doros_reward': ex_data.get('doros_reward', 20),
                }
                if ex_qs.exists():
                    ex_obj = ex_qs.first()
                    for k, v in ex_defaults.items():
                        setattr(ex_obj, k, v)
                    ex_obj.save()
                else:
                    ex_obj = Exercise.objects.create(
                        lesson=les_obj,
                        order=ex_data['order'],
                        **ex_defaults
                    )
                total_exercises += 1

                # Testovacie prípady cvičenia (vyčistíme existujúce a vložíme aktuálne)
                TestCase.objects.filter(exercise=ex_obj).delete()
                for tc_idx, tc_data in enumerate(ex_data.get('test_cases', []), start=1):
                    TestCase.objects.create(
                        exercise=ex_obj,
                        order=tc_data.get('order', tc_idx),
                        input_data=tc_data.get('input_data', ''),
                        expected_output=tc_data.get('expected_output', ''),
                        test_code=tc_data.get('test_code', ''),
                        is_hidden=tc_data.get('is_hidden', False),
                    )
                    total_test_cases += 1

    print(f"📖 Načítaných {total_modules} modulov, {total_lessons} lekcií, {total_quizzes} kvízov, {total_exercises} cvičení a {total_test_cases} testovacích prípadov!")

    # ==================================================================
    # 5. UČITEĽSKÝ OBCHOD S ODMENAMI A SKLADOVÝM HOSPODÁRSTVOM
    # ==================================================================
    RewardItem.objects.update_or_create(
        title_sk='Žolík: Odpustenie domácej úlohy',
        defaults={
            'title_en': 'Joker: Homework Pass',
            'description_sk': 'Umožňuje vynechať 1 domácu úlohu bez straty bodov. Obmedzená zásoba pre triedu!',
            'description_en': 'Allows skipping 1 homework assignment without penalty. Limited class stock!',
            'cost_doros': 250,
            'icon_name': 'bi-shield-check',
            'max_stock': 2,
            'current_stock': 2,
            'restock_period': RewardItem.RestockPeriod.WEEKLY,
            'limit_per_student_per_period': 1,
            'created_by': teacher
        }
    )

    RewardItem.objects.update_or_create(
        title_sk='+10 % bodov k praktickej písomke',
        defaults={
            'title_en': '+10% Bonus Points on Practical Exam',
            'description_sk': 'Pripočíta 10 % bonusových bodov k najbližšiemu testu z programovania.',
            'description_en': 'Adds 10% bonus points to your next coding test.',
            'cost_doros': 500,
            'icon_name': 'bi-graph-up-arrow',
            'max_stock': 1,
            'current_stock': 1,
            'restock_period': RewardItem.RestockPeriod.MONTHLY,
            'limit_per_student_per_period': 1,
            'created_by': teacher
        }
    )

    RewardItem.objects.update_or_create(
        title_sk='Nápoveda od učiteľa počas písomky',
        defaults={
            'title_en': 'Teacher Hint During Test',
            'description_sk': 'Učiteľ ti počas praktického testu pomôže odhaliť 1 chybu v kóde (Obnovuje sa denne).',
            'description_en': 'The teacher will help you debug 1 issue during a test (Restocks daily).',
            'cost_doros': 180,
            'icon_name': 'bi-lightbulb-fill',
            'max_stock': 2,
            'current_stock': 2,
            'restock_period': RewardItem.RestockPeriod.DAILY,
            'limit_per_student_per_period': 1,
            'created_by': teacher
        }
    )

    # ==================================================================
    # 6. OSOBNÉ QUESTY (DAILY, WEEKLY, MONTHLY)
    # ==================================================================
    Quest.objects.update_or_create(
        title_sk='Ranná rozcvička: Vyrieš 1 cvičenie',
        defaults={
            'title_en': 'Morning Warmup: Solve 1 Exercise',
            'period': Quest.QuestPeriod.DAILY,
            'metric_type': Quest.MetricType.SOLVE_EXERCISES,
            'target_value': 1,
            'reward_doros': 40,
            'reward_xp': 25
        }
    )
    Quest.objects.update_or_create(
        title_sk='Týždenný šprint: Nazbieraj 150 XP',
        defaults={
            'title_en': 'Weekly Sprint: Earn 150 XP',
            'period': Quest.QuestPeriod.WEEKLY,
            'metric_type': Quest.MetricType.EARN_XP,
            'target_value': 150,
            'reward_doros': 150,
            'reward_xp': 80
        }
    )
    Quest.objects.update_or_create(
        title_sk='Mesačný majster: Vyrieš 5 úloh na 1. pokus',
        defaults={
            'title_en': 'Monthly Master: Solve 5 Tasks on 1st Try',
            'period': Quest.QuestPeriod.MONTHLY,
            'metric_type': Quest.MetricType.FIRST_TRY_SOLVES,
            'target_value': 5,
            'reward_doros': 400,
            'reward_xp': 200
        }
    )

    # ==================================================================
    # 7. KOLEKTÍVNY TRIEDNY QUEST PRE IV.C
    # ==================================================================
    ClassQuest.objects.update_or_create(
        school_class=school_class,
        title_sk='Spoločná výzva IV.C: 20 vyriešených úloh za týždeň',
        defaults={
            'title_en': 'IV.C Class Quest: 20 Solved Tasks This Week',
            'period': Quest.QuestPeriod.WEEKLY,
            'target_exercises_count': 20,
            'current_exercises_count': 14,
            'reward_policy': ClassQuest.RewardPolicy.CONTRIBUTORS_ONLY,
            'min_contribution_required': 1,
            'reward_doros_per_student': 200,
            'deadline': timezone.now() + timedelta(days=5)
        }
    )

    # ==================================================================
    # 8. AKTÍVNY COIN DROP
    # ==================================================================
    CoinDrop.objects.update_or_create(
        title_sk='Popoludňajší Bonus Drop za aktivitu!',
        defaults={
            'title_en': 'Afternoon Activity Bonus Drop!',
            'school_class': school_class,
            'available_from': timezone.now() - timedelta(minutes=15),
            'available_until': timezone.now() + timedelta(hours=12),
            'max_claims': 5,
            'min_doros': 40,
            'max_doros': 120,
            'created_by': teacher
        }
    )

    # 9. Úvodná transakcia v peňaženke
    if not DorosTransaction.objects.filter(student=student).exists():
        DorosTransaction.objects.create(
            student=student,
            amount=350,
            reason_sk='Štartovací bonus a odmeny za doterajšiu aktivitu',
            reason_en='Starter bonus and activity rewards'
        )

    print("✅ Databáza Codoro bola úspešne naplnená všetkými 18 modulmi, odznakmi a odmenami!")
    print("👉 Prihlásenie UČITEĽ:  meno: ucitel  | heslo: heslo123")
    print("👉 Prihlásenie ŠTUDENT: meno: student | heslo: heslo123")


if __name__ == '__main__':
    run_seed()