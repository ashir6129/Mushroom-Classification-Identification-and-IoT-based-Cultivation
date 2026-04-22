"use client";

import { motion } from "framer-motion";

const otherSkills = [
    { title: "Creative Modeling", desc: "Exploring 3D design and visual arts", status: "Exploring", icon: "🎨" },
    { title: "Personal Branding", desc: "Building professional presence", status: "Active", icon: "🌟" },
    { title: "Visual Presentation", desc: "Creating impactful visual content", status: "Active", icon: "📊" },
    { title: "Content Creation", desc: "Technical writing and sharing", status: "Learning", icon: "✍️" },
    { title: "UI/UX Thinking", desc: "User-centered design principles", status: "Active", icon: "🎯" },
    { title: "Public Speaking", desc: "Presenting ideas confidently", status: "Developing", icon: "🎤" },
];

const statusColors: Record<string, string> = {
    Active: "bg-green-500/10 text-green-400 border-green-500/20",
    Learning: "bg-yellow-500/10 text-yellow-400 border-yellow-500/20",
    Exploring: "bg-purple-500/10 text-purple-400 border-purple-500/20",
    Developing: "bg-blue-500/10 text-blue-400 border-blue-500/20",
};

export function OtherSkillsSection() {
    return (
        <section className="py-64 sm:py-96 px-4 sm:px-6 lg:px-8 relative overflow-hidden bg-[var(--bg-secondary)]">
            {/* Subtle top border */}
            <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-pink-500/40 to-transparent" />

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
                        <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-pink-500/10 border border-pink-500/20 text-pink-400 text-sm font-medium mb-6">
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                            </svg>
                            Future-Ready
                        </span>
                        <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-[var(--text-primary)] mb-4">
                            My Other <span className="bg-gradient-to-r from-pink-400 to-orange-400 bg-clip-text text-transparent">Skills</span>
                        </h2>
                        <p className="text-lg text-[var(--text-secondary)] max-w-xl mx-auto">
                            I&apos;m not limited to CS. These are domains I&apos;m actively exploring.
                        </p>
                    </motion.div>

                    {/* Skills Grid */}
                    <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
                        {otherSkills.map((skill, i) => (
                            <motion.div
                                key={skill.title}
                                initial={{ opacity: 0, y: 30 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }}
                                transition={{ duration: 0.5, delay: i * 0.08 }}
                                className="relative p-5 bg-[var(--bg-card)] border border-[var(--border-subtle)] rounded-xl hover:border-pink-500/30 transition-all w-full"
                            >
                                <span className={`absolute top-3 right-3 px-2 py-0.5 text-[10px] font-medium rounded-full border ${statusColors[skill.status]}`}>
                                    {skill.status}
                                </span>
                                <span className="text-2xl mb-3 block">{skill.icon}</span>
                                <h3 className="font-semibold text-[var(--text-primary)] mb-1 text-sm">{skill.title}</h3>
                                <p className="text-xs text-[var(--text-tertiary)]">{skill.desc}</p>
                            </motion.div>
                        ))}
                    </div>

                    {/* Quote */}
                    <motion.p
                        initial={{ opacity: 0 }}
                        whileInView={{ opacity: 1 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6, delay: 0.3 }}
                        className="text-[var(--text-muted)] italic mt-10"
                    >
                        &ldquo;I can enter any field if I decide to.&rdquo;
                    </motion.p>
                </div>
            </div>

            {/* Subtle bottom border */}
            <div className="absolute bottom-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-pink-500/40 to-transparent" />
        </section>
    );
}
