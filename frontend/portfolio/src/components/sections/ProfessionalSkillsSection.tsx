"use client";

import { motion } from "framer-motion";

const professionalSkills = [
    { icon: "💬", title: "Communication", desc: "Clear articulation of complex ideas" },
    { icon: "🤝", title: "Teamwork", desc: "Collaborative and supportive mindset" },
    { icon: "🔄", title: "Adaptability", desc: "Quick to adjust to new challenges" },
    { icon: "🧩", title: "Problem Solving", desc: "Analytical approach to solutions" },
    { icon: "✅", title: "Ownership", desc: "Seeing projects through completion" },
    { icon: "📚", title: "Learning Agility", desc: "Rapid acquisition of new skills" },
];

export function ProfessionalSkillsSection() {
    return (
        <section className="py-64 sm:py-96 px-4 sm:px-6 lg:px-8 relative overflow-hidden bg-[var(--bg-primary)]">
            {/* Subtle top border */}
            <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-blue-500/40 to-transparent" />

            <div className="flex justify-center">
                <div className="relative w-full max-w-4xl text-center">
                    {/* Section Header */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6 }}
                        className="mb-12"
                    >
                        <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-sm font-medium mb-6">
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                            </svg>
                            Beyond Code
                        </span>
                        <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-[var(--text-primary)] mb-4">
                            Professional <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">Skills</span>
                        </h2>
                        <p className="text-lg text-[var(--text-secondary)] max-w-xl mx-auto">
                            The soft skills that make technical skills impactful.
                        </p>
                    </motion.div>

                    {/* Skills Grid */}
                    <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
                        {professionalSkills.map((skill, i) => (
                            <motion.div
                                key={skill.title}
                                initial={{ opacity: 0, y: 30 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }}
                                transition={{ duration: 0.5, delay: i * 0.08 }}
                                className="p-5 bg-[var(--bg-card)] border border-[var(--border-subtle)] rounded-xl hover:border-blue-500/30 transition-all w-full"
                            >
                                <span className="text-2xl mb-3 block">{skill.icon}</span>
                                <h3 className="font-semibold text-[var(--text-primary)] mb-1">{skill.title}</h3>
                                <p className="text-xs text-[var(--text-tertiary)]">{skill.desc}</p>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Subtle bottom border */}
            <div className="absolute bottom-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-blue-500/40 to-transparent" />
        </section>
    );
}
