/* === This file is part of Calamares - <http://github.com/calamares> ===
 *
 *   Copyright 2015, Rohan Garg <rohan@garg.io>
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

#include "WebViewStep.h"

#include <QVariant>
#include <QWebView>

WebViewStep::WebViewStep( QObject* parent )
    : Calamares::ViewStep( parent )
{
    emit nextStatusChanged( true );
    m_view = new QWebView;
}


WebViewStep::~WebViewStep()
{
    if ( m_view && m_view->parent() == nullptr )
        m_view->deleteLater();
}


QString
WebViewStep::prettyName() const
{
    return m_prettyName;
}


QWidget*
WebViewStep::widget()
{
    return m_view;
}


void
WebViewStep::next()
{
    emit done();
}


void
WebViewStep::back()
{}


bool
WebViewStep::isNextEnabled() const
{
    return true;
}


bool
WebViewStep::isBackEnabled() const
{
    return true;
}


bool
WebViewStep::isAtBeginning() const
{
    return true;
}


bool
WebViewStep::isAtEnd() const
{
    return true;
}

void WebViewStep::onActivate()
{
  m_view->load(QUrl(m_url));
  m_view->show();
}

QList< Calamares::job_ptr >
WebViewStep::jobs() const
{
    return QList< Calamares::job_ptr >();
}


void
WebViewStep::setConfigurationMap( const QVariantMap& configurationMap )
{
  if ( configurationMap.contains("url") &&
       configurationMap.value("url").type() == QVariant::String )
    m_url = configurationMap.value("url").toString();

  if ( configurationMap.contains("prettyName") &&
       configurationMap.value("prettyName").type() == QVariant::String )
    m_prettyName = configurationMap.value("prettyName").toString();
}
