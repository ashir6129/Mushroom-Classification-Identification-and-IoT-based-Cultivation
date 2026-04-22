"use client";

import { motion } from "framer-motion";

const technicalSkillCategories = [
    {
        title: "Programming Languages",
        icon: "💻",
        skills: ["TypeScript", "JavaScript", "Python", "Dart", "Java", "C++", "SQL"],
    },
    {
        title: "Frameworks & Libraries",
        icon: "🚀",
        skills: ["React", "Next.js", "Flutter", "Node.js", "Express", "FastAPI", "Tailwind CSS"],
    },
    {
        title: "Databases",
        icon: "🗄️",
        skills: ["PostgreSQL", "MongoDB", "Firebase", "Supabase", "SQLite", "Redis"],
    },
    {
        title: "AI / Machine Learning",
        icon: "🤖",
        skills: ["PyTorch", "TensorFlow", "ONNX Runtime", "Scikit-learn", "Computer Vision", "NLP"],
    },
    {
        title: "Systems & Core CS",
        icon: "⚙️",
        skills: ["Data Structures", "Algorithms", "Operating Systems", "Computer Networks", "OOP", "System Design"],
    },
    {
        title: "Tools & Platforms",
        icon: "🛠️",
        skills: ["Git", "GitHub", "Docker", "Vercel", "Linux", "VS Code", "Figma"],
    },
];

export function TechnicalSkillsSection() {
    return (
        <section id="skills" className="py-64 sm:py-96 px-4 sm:px-6 lg:px-8 relative overflow-hidden bg-[var(--bg-secondary)]">
            {/* Subtle top border */}
            <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-violet-500/40 to-transparent" />

            <div className="flex justify-center">
                <div className="relative w-full max-w-5xl text-center">
                    {/* Section Header */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6 }}
                        className="mb-12"
                    >
                        <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-violet-500/10 border border-violet-500/20 text-violet-400 text-sm font-medium mb-6">
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                            </svg>
                            Technical Expertise
                        </span>
                        <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-[var(--text-primary)] mb-4">
                            Technical <span className="bg-gradient-to-r from-violet-400 to-purple-400 bg-clip-text text-transparent">Skills</span>
                        </h2>
                        <p className="text-lg text-[var(--text-secondary)] max-w-xl mx-auto">
                            Technologies and tools I use to bring ideas to life.
                        </p>
                    </motion.div>

                    {/* Skills Grid */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
                        {technicalSkillCategories.map((category, i) => (
                            <motion.div
                                key={category.title}
                                initial={{ opacity: 0, y: 30 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }}
                                transition={{ duration: 0.5, delay: i * 0.08 }}
                                className="p-5 bg-[var(--bg-card)] border border-[var(--border-subtle)] rounded-xl hover:border-violet-500/30 transition-all text-left w-full"
                            >
                                <div className="flex items-center gap-3 mb-4">
                                    <span className="text-xl">{category.icon}</span>
                                    <h3 className="font-semibold text-[var(--text-primary)] text-sm">
                                        {category.title}
                                    </h3>
                                </div>
                                <div className="flex flex-wrap gap-1.5">
                                    {category.skills.map((skill) => (
                                        <span
                                            key={skill}
                                            className="px-2.5 py-1 text-xs bg-[var(--bg-tertiary)] text-[var(--text-secondary)] rounded-md hover:bg-violet-500/10 hover:text-violet-400 transition-all cursor-default"
                                        >
                                            {skill}
                                        </span>
                                    ))}
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Subtle bottom border */}
            <div className="absolute bottom-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-violet-500/40 to-transparent" />
        </section>
    );
}
