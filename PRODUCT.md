# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Students learning Python are the primary users. They practice in an interactive editor, follow a guided curriculum, and earn Doros as they make progress. Teachers use Codoro to manage classes, monitor student work, and run shared classroom activities. This redesign gives the student experience the deepest workflow attention.

## Product Purpose

Codoro teaches Python through hands-on practice connected to real classroom learning. Students build skills through guided lessons and exercises, with teacher oversight and classroom rewards supporting their progress.

## Positioning

Codoro combines an interactive Python learning environment with classroom management, a Socratic AI tutor, and Doros that can be exchanged for teacher-managed classroom rewards. The user confirmed the student loop of coding, guided progression, and earned Doros, with teachers managing classrooms alongside it.

## Operating Context

Students use Codoro to study Python, solve tested exercises, consult the Codo tutor, track progress, and participate in classroom quests and rewards. Teachers manage students, classes, lessons, exercises, rewards, and classroom quests. The interface supports Slovak and English.

## Capabilities and Constraints

- Existing Django templates and routes provide public, student, teacher, and admin surfaces; this work changes the interface while preserving product behavior.
- Student capabilities include a Python editor, lessons, exercises, a curriculum map, practice arena, reference sheets, profile, and reward shop.
- Teacher capabilities include class and student management, curriculum authoring, exercise testing, and classroom rewards and quests.
- Codo is presented as a Socratic tutor. Doros are the existing reward currency.
- Existing Slovak and English content, Codoro identity assets, feature names, and functional workflows are product facts to preserve.

## Brand Commitments

Preserve the Codoro name, existing logo and Codo mascot assets, green landscape, and familiar page structure. Raise the visual craft without replacing Codoro's existing look. Keep the product terminology Codoro, Codo, and Doros.

## Evidence on Hand

- Product and audience copy: `templates/landing.html` and `templates/base.html`.
- Student workflows: `templates/courses/` and `templates/gamification/shop.html`.
- Teacher workflows: `templates/teacher_panel/`.
- Public logo and mascot assets: `static/img/`.
- User-confirmed student loop and teacher classroom role from this redesign request.

## Product Principles

- Students learn by writing and testing real Python code.
- Guided progression should make the next useful learning step clear.
- Teachers and students share the same classroom learning context.
- Rewards support learning progress and classroom participation.
- Core learning workflows remain usable in Slovak and English.

## Accessibility & Inclusion

The learning and classroom interfaces must work on mobile screens as well as desktop, with touch-friendly controls, keyboard access, and reduced-motion support.
