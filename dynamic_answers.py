"""Dynamic interview answer generator using rich contextual stories.

This module encapsulates a small knowledge base describing the user's
professional experiences across several organizations.  The
``DynamicAnswerGenerator`` class exposes a ``generate_answer`` method that takes
an interview prompt category and assembles a narrative that blends the
appropriate situational context, conflict, actions, and results.  The goal is to
mirror the functionality described in the user prompt where answers should go
beyond resume bullets and leverage deep institutional knowledge.

Example
-------
>>> generator = DynamicAnswerGenerator()
>>> print(generator.generate_answer("influence"))
"""

from __future__ import annotations

from dataclasses import dataclass
from textwrap import dedent
from typing import Dict, Iterable, List


@dataclass(frozen=True)
class Story:
    """Representation of a single interview story."""

    question_type: str
    hook: str
    situation: str
    action: str
    result: str
    takeaway: str

    def render(self) -> str:
        """Render the story as a single multi-paragraph answer."""

        return dedent(
            f"""
            {self.hook}

            Situation: {self.situation}
            Action: {self.action}
            Result: {self.result}
            Takeaway: {self.takeaway}
            """
        ).strip()


class DynamicAnswerGenerator:
    """Generate interview answers that combine multiple experience stories.

    The generator stores a catalog of stories grouped by a canonical
    ``question_type`` string.  When ``generate_answer`` is called the best story
    for the requested type is returned.  The current implementation keeps a
    single story per question type, but the design allows for future expansion
    where multiple stories can be rotated or tailored on the fly.
    """

    def __init__(self) -> None:
        self._stories: Dict[str, List[Story]] = {}
        self._register_default_stories()

    # ------------------------------------------------------------------
    # Registration helpers
    # ------------------------------------------------------------------
    def _register_default_stories(self) -> None:
        """Populate the generator with curated, high-context stories."""

        self.register_story(
            Story(
                question_type="influence",
                hook=(
                    "At Southwest Airlines I routinely found myself translating between "
                    "operations and finance leadership during a period of intense "
                    "operational disruption."
                ),
                situation=(
                    "Severe weather, pandemic aftershocks, and crew scheduling volatility "
                    "created a gulf between the operational metrics reported in real time "
                    "and the GAAP narratives investors needed."
                ),
                action=(
                    "I built an 'Operational Reality Dashboard' that overlaid flight "
                    "performance, crew utilization, and fuel spikes with their direct "
                    "impact on quarterly forecasts.  I facilitated joint reviews so "
                    "operations leaders could see the financial stakes and finance could "
                    "ask about operational constraints before numbers were finalized."
                ),
                result=(
                    "Forecast accuracy improved by 40% and both teams started flagging "
                    "potential issues to each other two weeks earlier than before, "
                    "preventing several investor-relations fire drills."
                ),
                takeaway=(
                    "Influence without authority means building shared language; the "
                    "dashboard made every leader feel heard and aligned."
                ),
            )
        )

        self.register_story(
            Story(
                question_type="failure",
                hook=(
                    "During my tenure with the NYC Department of Education I learned the "
                    "hard way that a technically perfect model can still fail politically."
                ),
                situation=(
                    "I spent weeks engineering a capital-allocation model for 1,800 "
                    "schools, balancing enrollment projections, facility conditions, and "
                    "equity goals.  The analysis ignored community dynamics that district "
                    "leaders navigated daily."
                ),
                action=(
                    "After the initial rollout flopped, I interviewed principals, sat in on "
                    "community board sessions, and re-framed the same data around "
                    "neighborhood priorities and compliance constraints."
                ),
                result=(
                    "Approvals accelerated by 25% because stakeholders finally saw their "
                    "concerns reflected in the plan."
                ),
                takeaway=(
                    "Data only drives change when paired with empathy; now I co-create "
                    "insights with the people they affect."
                ),
            )
        )

        self.register_story(
            Story(
                question_type="tradeoff",
                hook=(
                    "At LinkedIn, I frequently mediated the tension between rapid user "
                    "growth and the trust & safety controls that keep the platform "
                    "credible."
                ),
                situation=(
                    "A planned policy change promised significant sign-up growth but "
                    "risked exposing members to more fraudulent outreach."
                ),
                action=(
                    "I quantified the projected member-value erosion, built a risk-adjusted "
                    "growth model, and brokered workshops with product, legal, and trust & "
                    "safety leads to pressure-test mitigation ideas."
                ),
                result=(
                    "We launched with additional verification checkpoints and saved an "
                    "estimated $2M in fraud losses while still hitting 90% of the original "
                    "growth target."
                ),
                takeaway=(
                    "Balancing growth and safety requires framing tradeoffs in shared "
                    "metrics so every stakeholder can co-own the decision."
                ),
            )
        )

    def register_story(self, story: Story) -> None:
        """Register a story for one or more question types."""

        self._stories.setdefault(story.question_type.lower(), []).append(story)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def available_question_types(self) -> Iterable[str]:
        """Return the list of available question categories."""

        return self._stories.keys()

    def generate_answer(self, question_type: str) -> str:
        """Generate an answer for the requested question category.

        Parameters
        ----------
        question_type:
            Case-insensitive question category (e.g. ``"influence"``).

        Returns
        -------
        str
            The highest-priority story rendered as a formatted narrative.

        Raises
        ------
        KeyError
            If the requested question category has no registered stories.
        """

        normalized = question_type.lower()
        try:
            story = self._stories[normalized][0]
        except KeyError as exc:
            available = ", ".join(sorted(self._stories)) or "none"
            raise KeyError(
                f"No stories registered for '{question_type}'. Available types: {available}."
            ) from exc

        return story.render()


def demo() -> None:
    """Simple CLI demo that prints all available stories."""

    generator = DynamicAnswerGenerator()
    for question_type in generator.available_question_types():
        print("=" * 80)
        print(f"Question Type: {question_type}\n")
        print(generator.generate_answer(question_type))
        print()


if __name__ == "__main__":
    demo()
