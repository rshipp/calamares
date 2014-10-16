/* === This file is part of Calamares - <http://github.com/calamares> ===
 *
 *   Copyright 2014, Teo Mrnjavac <teo@kde.org>
 *
 *   Calamares is free software: you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation, either version 3 of the License, or
 *   (at your option) any later version.
 *
 *   Calamares is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with Calamares. If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef BRANDING_H
#define BRANDING_H

#include "UiDllMacro.h"
#include "Typedefs.h"

#include <QObject>
#include <QStringList>
#include <QMap>


namespace Calamares
{

class UIDLLEXPORT Branding : public QObject
{
    Q_OBJECT
public:
    enum StringEntry : short
    {
        ProductName,
        Version,
        ShortVersion,
        VersionedName,
        ShortVersionedName
    };

    enum ImageEntry : short
    {
        ProductLogo,
        ProductIcon
    };

    static Branding* instance();

    explicit Branding( const QString& brandingFilePath,
                       QObject *parent = nullptr );

    QString descriptorPath() const;
    QString componentName() const;
    QString componentDirectory() const;

    QString string( Branding::StringEntry stringEntry ) const;
    QString imagePath( Branding::ImageEntry imageEntry ) const;
    QPixmap image( Branding::ImageEntry imageEntry, const QSize& size ) const;
    QStringList slideshowPaths() const;

private:
    static Branding* s_instance;

    static QStringList s_stringEntryStrings;
    static QStringList s_imageEntryStrings;

    void bail( const QString& message );

    QString m_descriptorPath;
    QString m_componentName;
    QMap< QString, QString > m_strings;
    QMap< QString, QString > m_images;
    QStringList m_slideshow;
};

}

#endif // BRANDING_H