"use client";

import { useState, useMemo } from "react";
import { motion } from "framer-motion";
import { Project } from "@/types";
import { ProjectCard, ProjectCardSkeleton } from "@/components/ui";
import { getLanguageColor } from "@/lib/github";

interface ProjectsGridProps {
    projects: Project[];
}

export function ProjectsGrid({ projects }: ProjectsGridProps) {
    const [search, setSearch] = useState("");
    const [selectedLanguage, setSelectedLanguage] = useState<string | null>(null);
    const [sortBy, setSortBy] = useState<"stars" | "recent">("recent");

    // Get unique languages
    const languages = useMemo(() => {
        const langs = projects
            .map((p) => p.language)
            .filter((lang): lang is string => lang !== null);
        return [...new Set(langs)].sort();
    }, [projects]);

    // Filter and sort projects
    const filteredProjects = useMemo(() => {
        let result = [...projects];

        // Search filter
        if (search) {
            const searchLower = search.toLowerCase();
            result = result.filter(
                (p) =>
                    p.name.toLowerCase().includes(searchLower) ||
                    p.description?.toLowerCase().includes(searchLower) ||
                    p.topics.some((t) => t.toLowerCase().includes(searchLower))
            );
        }

        // Language filter
        if (selectedLanguage) {
            result = result.filter((p) => p.language === selectedLanguage);
        }

        // Sort
        result.sort((a, b) => {
            if (sortBy === "stars") {
                return b.stars - a.stars;
            }
            return new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime();
        });

        return result;
    }, [projects, search, selectedLanguage, sortBy]);

    return (
        <div>
            {/* Filters */}
            <div className="flex flex-col md:flex-row gap-4 mb-8">
                {/* Search */}
                <div className="relative flex-1">
                    <svg
                        className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-[var(--text-muted)]"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                        />
                    </svg>
                    <input
                        type="text"
                        placeholder="Search projects..."
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                        className="w-full pl-12 pr-4 py-3 bg-[var(--bg-card)] border border-[var(--border-subtle)] rounded-xl text-[var(--text-primary)] placeholder:text-[var(--text-muted)] focus:outline-none focus:border-[var(--accent-primary)] transition-colors"
                    />
                </div>

                {/* Language Filter */}
                <select
                    value={selectedLanguage || ""}
                    onChange={(e) => setSelectedLanguage(e.target.value || null)}
                    className="px-4 py-3 bg-[var(--bg-card)] border border-[var(--border-subtle)] rounded-xl text-[var(--text-primary)] focus:outline-none focus:border-[var(--accent-primary)] transition-colors cursor-pointer"
                >
                    <option value="">All Languages</option>
                    {languages.map((lang) => (
                        <option key={lang} value={lang}>
                            {lang}
                        </option>
                    ))}
                </select>

                {/* Sort */}
                <select
                    value={sortBy}
                    onChange={(e) => setSortBy(e.target.value as "stars" | "recent")}
                    className="px-4 py-3 bg-[var(--bg-card)] border border-[var(--border-subtle)] rounded-xl text-[var(--text-primary)] focus:outline-none focus:border-[var(--accent-primary)] transition-colors cursor-pointer"
                >
                    <option value="recent">Most Recent</option>
                    <option value="stars">Most Stars</option>
                </select>
            </div>

            {/* Active Filters */}
            {(search || selectedLanguage) && (
                <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: "auto" }}
                    className="flex flex-wrap items-center gap-2 mb-6"
                >
                    <span className="text-sm text-[var(--text-muted)]">Active filters:</span>
                    {search && (
                        <button
                            onClick={() => setSearch("")}
                            className="inline-flex items-center gap-1 px-2 py-1 text-xs bg-[var(--bg-card)] border border-[var(--border-subtle)] rounded-full hover:border-[var(--accent-primary)] transition-colors"
                        >
                            Search: &quot;{search}&quot;
                            <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    )}
                    {selectedLanguage && (
                        <button
                            onClick={() => setSelectedLanguage(null)}
                            className="inline-flex items-center gap-1 px-2 py-1 text-xs bg-[var(--bg-card)] border border-[var(--border-subtle)] rounded-full hover:border-[var(--accent-primary)] transition-colors"
                        >
                            <span
                                className="w-2 h-2 rounded-full"
                                style={{ backgroundColor: getLanguageColor(selectedLanguage) }}
                            />
                            {selectedLanguage}
                            <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    )}
                    <button
                        onClick={() => {
                            setSearch("");
                            setSelectedLanguage(null);
                        }}
                        className="text-xs text-[var(--accent-primary)] hover:underline"
                    >
                        Clear all
                    </button>
                </motion.div>
            )}

            {/* Results Count */}
            <p className="text-sm text-[var(--text-muted)] mb-6">
                Showing {filteredProjects.length} of {projects.length} projects
            </p>

            {/* Projects Grid */}
            {filteredProjects.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {filteredProjects.map((project, index) => (
                        <ProjectCard key={project.id} project={project} index={index} />
                    ))}
                </div>
            ) : (
                <div className="text-center py-16">
                    <div className="text-4xl mb-4">🔍</div>
                    <h3 className="heading-sm mb-2">No projects found</h3>
                    <p className="body-sm">Try adjusting your search or filters</p>
                </div>
            )}
        </div>
    );
}
