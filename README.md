# Asadbek Xodjayev

Computer Science and Economics student at Webster University (B.S. and B.A., expected May 2027), studying at the Tashkent campus.

I train small language models from scratch and test whether they compute answers or only remember them. I also build software, and I like games.

Applying to research-based MSc programmes for Fall 2027.

## Research

**[MathGen](https://github.com/asadbekXodjayev/math-v)**: a decoder-only transformer trained from scratch on synthetic mathematics, on a 4 GB laptop GPU. RoPE, SwiGLU, RMSNorm and a custom BPE tokenizer, all written in PyTorch.

My first model scored about 80%. An audit showed that 48.8% of its validation samples were exact copies of training samples, so that number measured memorization. I rebuilt the evaluation with hash-based splits, held-out value blocks and longer operands.

Pilot results (about 5M parameters, 5 seeds):

- 99.7% on problems seen in training
- 92.0% on unseen problems in the training range
- 39.4% on value blocks held out from training
- 0.3% when operands have one more digit

These are pilot runs. The full study and report are in progress.

## Open source (merged)

- **NVIDIA/Megatron-LM** [#5445](https://github.com/NVIDIA/Megatron-LM/pull/5445): fixed infinite recursion in the abstract tokenizer's special-token-ID property aliases.
- **NVIDIA/SkillSpector** [#166](https://github.com/NVIDIA/SkillSpector/pull/166) and [#167](https://github.com/NVIDIA/SkillSpector/pull/167): detection of reflective `exec` through `getattr()` literals, and of Unicode Tag-block "ASCII smuggling" hidden instructions in AI-agent skills.

## Open source (proposal adopted)

- **alirezarezvani/claude-skills** [#849](https://github.com/alirezarezvani/claude-skills/issues/849): proposed an i18n and localization skill. The maintainer built it as the `i18n-localization` plugin ([#1095](https://github.com/alirezarezvani/claude-skills/pull/1095)) and released it in [v2.14.7](https://github.com/alirezarezvani/claude-skills/releases/tag/v2.14.7).

## Engineering and teaching

- Three years building production web platforms in React and TypeScript, mainly for logistics companies.
- Instructor at IT-Academy, Tashkent (2023 to 2025): taught web development and ran code reviews.
- Built a math-learning web app, whose problem generators became the engine of MathGen.

## Tools

Python, PyTorch, C++, C#, TypeScript, React, Git

## Find me

[Website](https://asadbek.xodjayev.uz) · [CV (PDF)](https://asadbek.xodjayev.uz/docs/Asadbek_Xodjayev_CV.pdf) · [LinkedIn](https://www.linkedin.com/in/asadbek-xodjayev-1bb8a624a/) · asadbekxodjayev@webster.edu
