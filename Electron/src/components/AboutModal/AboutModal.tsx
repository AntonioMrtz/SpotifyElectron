"use client"

import type React from "react"
import { Dialog, DialogTitle, DialogContent, IconButton, Typography, Box, Chip, Button, Avatar } from "@mui/material"
import {
    Close as CloseIcon,
    Headphones as HeadphonesIcon,
    GitHub as GitHubIcon,
    Language as WebIcon,
    MenuBook as DocsIcon,
    Person as PersonIcon,
    Star as StarIcon,
    Launch as LaunchIcon,
} from "@mui/icons-material"
import { t } from "i18next"
import Global from "global/global"
import styles from "./AboutModal.module.css"

interface AboutModalProps {
    open: boolean
    onClose: () => void
}

const AboutModal: React.FC<AboutModalProps> = ({ open, onClose }) => {
    // Get version safely with fallback
    let APP_VERSION = "v1.0.0"
    try {
        APP_VERSION = Global.APPVERSION || "v1.0.0"
    } catch (error) {
        APP_VERSION = "v1.0.0"
    }

    const GITHUB_REPO = Global.repositoryUrl || "https://github.com/AntonioMrtz/SpotifyElectron"
    const APP_WEBSITE = "https://your-website.com"
    const DOCS_URL = "https://your-docs.com"

    const handleExternalLink = (url: string) => {
        window.open(url, "_blank")
    }

    const socialLinks = [
        {
            name: "Twitter",
            url: "https://twitter.com/AntonioMrtz",
            icon: "🐦",
        },
        {
            name: "LinkedIn",
            url: "https://linkedin.com/in/antoniomrtz",
            icon: "💼",
        },
        {
            name: "Email",
            url: "mailto:contact@antoniomrtz.com",
            icon: "✉️",
        },
    ]

    const projectLinks = [
        {
            name: t("aboutModal.officialWebsite", "Official Website"),
            url: APP_WEBSITE,
            icon: <WebIcon className={styles.linkButtonIcon} />,
            description: "Visit our main website",
        },
        {
            name: t("aboutModal.githubRepository", "GitHub Repository"),
            url: GITHUB_REPO,
            icon: <GitHubIcon className={styles.linkButtonIcon} />,
            description: "View source code and contribute",
        },
        {
            name: t("aboutModal.documentation", "Documentation"),
            url: DOCS_URL,
            icon: <DocsIcon className={styles.linkButtonIcon} />,
            description: "Learn how to use the app",
        },
    ]

    return (
        <Dialog
            open={open}
            onClose={onClose}
            maxWidth="sm"
            fullWidth
            className={styles.aboutModal}
            BackdropProps={{
                className: styles.modalBackdrop,
            }}
            PaperProps={{
                className: styles.modalPaper,
            }}
        >
            {/* Header */}
            <DialogTitle className={styles.modalHeader} sx={{ p: 0, m: 0 }}>
                <Box className={styles.headerTitle}>
                    <HeadphonesIcon className={styles.appIcon} />
                    <Box>
                        <Typography variant="h6" className={styles.title}>
                            {t("aboutModal.title", "Spotify Electron")}
                        </Typography>
                        <Typography variant="caption" className={styles.secondaryText}>
                            Your music, reimagined
                        </Typography>
                    </Box>
                </Box>
                <IconButton onClick={onClose} className={styles.closeButton} aria-label="Close about dialog">
                    <CloseIcon />
                </IconButton>
            </DialogTitle>

            <DialogContent className={styles.modalContent}>
                {/* Version Section */}
                <Box sx={{ textAlign: "center", mb: 3 }}>
                    <Chip
                        label={t("aboutModal.version", {
                            version: APP_VERSION,
                            defaultValue: `Version ${APP_VERSION}`
                        })}
                        className={styles.versionChip}
                    />
                </Box>

                {/* Links Section */}
                <Box className={`${styles.section} ${styles.sectionFirst}`}>
                    <Typography variant="subtitle1" className={styles.sectionTitle}>
                        {t("aboutModal.projectLinks", "Project Links")}
                    </Typography>

                    <Box sx={{ display: "flex", flexDirection: "column" }}>
                        {projectLinks.map((link, index) => (
                            <Button
                                key={index}
                                startIcon={link.icon}
                                endIcon={<LaunchIcon sx={{ fontSize: 16, opacity: 0.7 }} />}
                                onClick={() => handleExternalLink(link.url)}
                                className={styles.linkButton}
                            >
                                <Box sx={{ flex: 1, textAlign: "left" }}>
                                    <Typography component="span" sx={{ fontWeight: 600, display: "block" }}>
                                        {link.name}
                                    </Typography>
                                    <Typography component="span" className={styles.secondaryText} sx={{ fontSize: "0.8rem" }}>
                                        {link.description}
                                    </Typography>
                                </Box>
                            </Button>
                        ))}
                    </Box>
                </Box>

                {/* Developer Section */}
                <Box className={styles.section}>
                    <Typography variant="subtitle1" className={styles.sectionTitle}>
                        <PersonIcon sx={{ color: "var(--spotify-green, #1db954)", mr: 1, fontSize: 20 }} />
                        {t("aboutModal.createdBy", "Meet the Developer")}
                    </Typography>

                    <Box className={styles.developerSection}>
                        <Avatar className={styles.developerAvatar}>AM</Avatar>
                        <Box sx={{ flex: 1 }}>
                            <Typography className={styles.primaryText}>AntonioMrtz</Typography>
                            <Typography className={styles.secondaryText}>
                                Full-stack developer passionate about music and technology
                            </Typography>
                        </Box>
                    </Box>

                    <Typography className={styles.secondaryText} sx={{ mb: 2, fontSize: "0.85rem" }}>
                        {t("aboutModal.connectDeveloper", "Connect with the developer on social media:")}
                    </Typography>

                    <Box className={styles.socialLinksContainer}>
                        {socialLinks.map((social) => (
                            <Button
                                key={social.name}
                                size="small"
                                onClick={() => handleExternalLink(social.url)}
                                className={styles.socialButton}
                            >
                                {social.icon} {social.name}
                            </Button>
                        ))}
                    </Box>
                </Box>

                {/* Star Section */}
                <Box className={styles.ctaSection}>
                    <Typography className={styles.secondaryText} sx={{ mb: 3, fontWeight: 500 }}>
                        {t("aboutModal.supportText", "Love this project? Help us grow by starring it on GitHub!")}
                    </Typography>

                    <Button
                        variant="contained"
                        startIcon={<StarIcon />}
                        endIcon={<GitHubIcon sx={{ ml: 0.5 }} />}
                        onClick={() => handleExternalLink(GITHUB_REPO)}
                        className={styles.starButton}
                    >
                        {t("aboutModal.starButton", "Star on GitHub")}
                    </Button>
                </Box>
            </DialogContent>
        </Dialog>
    )
}

export default AboutModal
